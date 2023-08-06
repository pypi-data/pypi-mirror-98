#!/usr/bin/env python

"""Utility classes."""

import crypt
import logging
import os
import random
import string

from contextlib import contextmanager

from http.client import HTTPSConnection
from importlib.resources import read_text
from pathlib import Path
from random import randrange
from shutil import copyfile
from socket import getfqdn
from ssl import SSLContext
from tempfile import NamedTemporaryFile
from time import time
from typing import Dict, Generator, List, NamedTuple
from urllib.parse import quote, urlparse, urlunparse

from certifi import where
from OpenSSL import crypto
from _pytest.tmpdir import TempPathFactory
from lovely.pytest.docker.compose import Services


LOGGER = logging.getLogger(__name__)

DOCKER_GIT_SERVICE = "pytest-docker-git"
DOCKER_GIT_SERVICE_PATTERN = f"{DOCKER_GIT_SERVICE}-{{0}}-{{1}}"


class CertificateKeypair(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: bytes
    ca_private_key: bytes
    certificate: bytes
    private_key: bytes


def check_url_secure(
    docker_ip: str,
    public_port: int,
    *,
    auth_header: Dict[str, str],
    ssl_context: SSLContext,
) -> bool:
    """
    Secure form of lovey/pytest/docker/compose.py::check_url() that checks when the secure docker GIT service is
    operational.

    Args:
        docker_ip: IP address on which the service is exposed.
        public_port: Port on which the service is exposed.
        auth_header: HTTP basic authentication header to using when connecting to the service.
        ssl_context:
            SSL context referencing the trusted root CA certificated to used when negotiating the TLS connection.

    Returns:
        (bool) True when the service is operational, False otherwise.
    """
    try:
        https_connection = HTTPSConnection(
            context=ssl_context, host=docker_ip, port=public_port
        )
        https_connection.request("HEAD", "/v2/", headers=auth_header)
        return https_connection.getresponse().status < 500
    except Exception:  # pylint: disable=broad-except
        return False


def generate_cacerts(
    tmp_path_factory: TempPathFactory,
    *,
    certificate: Path,
    delete_after: bool = True,
) -> Generator[Path, None, None]:
    """
    Generates a temporary CA certificate trust store containing a given certificate.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        certificate: Path to the certificate to be included in the trust store.
        delete_after: If True, the temporary file will be removed after the iteration is complete.

    Yields:
        The path to the temporary file.
    """
    # Note: where() path cannot be trusted to be temporary, don't pollute persistent files ...
    name = DOCKER_GIT_SERVICE_PATTERN.format("cacerts", "x")
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath(name)
    copyfile(where(), tmp_path)

    with certificate.open("r") as file_in:
        with tmp_path.open("w") as file_out:
            file_out.write(file_in.read())
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def generate_htpasswd(
    tmp_path_factory: TempPathFactory,
    *,
    delete_after: bool = True,
    password: str,
    username: str,
) -> Generator[Path, None, None]:
    """
    Generates a temporary htpasswd containing a given set of credentials.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        password: The password corresponding to the provided user name.
        username: The name of the user to include in the htpasswd file.

    Yields:
        The path to the temporary file.
    """
    # TODO: Why doesn't apache2 like $2b$ hashes?!?
    # hashpw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()
    salt = "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(2)
    )
    hashpw = crypt.crypt(password, salt)
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath("htpasswd")
    with tmp_path.open("w") as file:
        file.write(f"{username}:{hashpw}")
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def generate_keypair(
    *, keysize: int = 4096, life_cycle: int = 7 * 24 * 60 * 60
) -> CertificateKeypair:
    """
    Generates a keypair and certificate for the GIT service.

    Args:
        keysize: size of the private key.
        life_cycle: Lifespan of the generated certificates, in seconds.

    Returns:
        tuple:
            certificate: The public certificate.
            private_key: The private key.
    """

    # Generate a self-signed certificate authority ...
    pkey_ca = crypto.PKey()
    pkey_ca.generate_key(crypto.TYPE_RSA, keysize)

    x509_ca = crypto.X509()
    x509_ca.get_subject().commonName = f"pytest-docker-git-fixtures-ca-{time()}"
    x509_ca.gmtime_adj_notBefore(0)
    x509_ca.gmtime_adj_notAfter(life_cycle)
    x509_ca.set_issuer(x509_ca.get_subject())
    x509_ca.set_pubkey(pkey_ca)
    x509_ca.set_serial_number(randrange(100000))
    x509_ca.set_version(2)

    x509_ca.add_extensions(
        [crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=x509_ca)]
    )
    x509_ca.add_extensions(
        [
            crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
            crypto.X509Extension(
                b"authorityKeyIdentifier", False, b"keyid:always", issuer=x509_ca
            ),
            crypto.X509Extension(
                b"keyUsage", True, b"digitalSignature, keyCertSign, cRLSign"
            ),
        ]
    )

    x509_ca.sign(pkey_ca, "sha256")

    # Generate a certificate ...
    pkey_cert = crypto.PKey()
    pkey_cert.generate_key(crypto.TYPE_RSA, keysize)

    x509_cert = crypto.X509()
    x509_cert.get_subject().commonName = getfqdn()
    x509_cert.gmtime_adj_notBefore(0)
    x509_cert.gmtime_adj_notAfter(life_cycle)
    x509_cert.set_issuer(x509_ca.get_subject())
    x509_cert.set_pubkey(pkey_cert)
    x509_cert.set_serial_number(randrange(100000))
    x509_cert.set_version(2)

    x509_cert.add_extensions(
        [
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
            crypto.X509Extension(b"extendedKeyUsage", False, b"serverAuth, clientAuth"),
            crypto.X509Extension(
                b"subjectAltName",
                False,
                ",".join(
                    [
                        f"DNS:{getfqdn()}",
                        f"DNS:*.{getfqdn()}",
                        "DNS:localhost",
                        "DNS:*.localhost",
                        "IP:127.0.0.1",
                    ]
                ).encode("utf-8"),
            ),
        ]
    )

    x509_cert.sign(pkey_ca, "sha256")

    return CertificateKeypair(
        ca_certificate=crypto.dump_certificate(crypto.FILETYPE_PEM, x509_ca),
        ca_private_key=crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey_ca),
        certificate=crypto.dump_certificate(crypto.FILETYPE_PEM, x509_cert),
        private_key=crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey_cert),
    )


def get_created_repos(request):
    """
    Retrieves the list of 'create_repo' pytest marks from a given request.

    Args:
        request: The pytest request from which to retrieve the marks.

    Returns:
        The list of created repositories.
    """
    mark = request.node.get_closest_marker("create_repo")
    return mark.args if mark else []


def get_docker_compose_user_defined(
    docker_compose_files: List[str], service_name: str
) -> Generator[Path, None, None]:
    """
    Tests to see if a user-defined configuration exists, and contains the docker GIT service name.

    Args:
        docker_compose_files: List of docker-compose.yml locations.
        service_name: Name of the docker GIT service.

    Yields:
        The path to a user-defined docker-compose.yml file that contains the service.
    """
    for docker_compose_file in [Path(x) for x in docker_compose_files]:
        try:
            if f"{service_name}:" in docker_compose_file.read_text():
                yield docker_compose_file
        except (FileNotFoundError, IOError):
            ...


def get_embedded_file(
    tmp_path_factory: TempPathFactory, *, delete_after: bool = True, name: str
) -> Generator[Path, None, None]:
    """
    Replicates a file embedded within this package to a temporary file.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        name: The name of the embedded file to be replicated.

    Yields:
        The path to the temporary file.
    """
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath(name)
    with tmp_path.open("w") as file:
        file.write(read_text(__package__, name))
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def get_mirrored_repos(request):
    """
    Retrieves the list of 'mirror_repo' pytest marks from a given request.

    Args:
        request: The pytest request from which to retrieve the marks.

    Returns:
        The list of mirrored repositories.
    """
    mark = request.node.get_closest_marker("mirror_repo")
    return mark.args if mark else []


def get_user_defined_file(pytestconfig: "_pytest.config.Config", name: str):
    """
    Tests to see if a user-defined file exists.

    Args:
        pytestconfig: pytest configuration file to use when locating the user-defined file.
        name: Name of the user-defined file.

    Yields:
        The path to the user-defined file.
    """
    user_defined = Path(str(pytestconfig.rootdir), "tests", name)
    if user_defined.exists():
        yield user_defined


def start_service(
    docker_services: Services,
    *,
    docker_compose: Path,
    port: int,
    service_name: str,
    **kwargs,
):
    # pylint: disable=protected-access
    """
    Instantiates a given service using docker-compose.

    Args:
        docker_services: lovely service to use to start the service.
        docker_compose: Path to the docker-compose configuration file (to be injected).
        port: Name of the service, within the docker-compose configuration, to be instantiated.
        service_name: The port, inside the container, on which the service is running.
    """
    # DUCK PUNCH: Don't get in the way of user-defined lovey/pytest/docker/compose.py::docker_compose_files()
    #             overrides ...
    docker_services._docker_compose._compose_files = [
        str(docker_compose)
    ]  # pylint: disable=protected-access
    docker_services.start(service_name)
    public_port = docker_services.wait_for_service(service_name, port, **kwargs)
    return f"{docker_services.docker_ip}:{public_port}"


@contextmanager
def git_askpass_script(
    tmp_path_factory: TempPathFactory, *, delete_after: bool = True, password: str
) -> Generator[Path, None, None]:
    """
    Context manage that initializes a temporary GIT askpass script.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        password: The password to be provided by the askpass script.

    Yields:
        The path to the temporary file.
    """
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath("git_askpass")
    with tmp_path.open("w") as file:
        file.write(f"echo {password}")
    tmp_path.chmod(0o700)
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


@contextmanager
def git_credentials_store(
    *, password: str, uri: str, username: str
) -> Generator[Path, None, None]:
    """Context manage that initializes a temporary GIT credentials store."""

    segments = urlparse(uri)
    segments = segments._replace(  # pylint: disable=protected-access
        netloc=f"{quote(username)}:{quote(password)}@{segments.netloc}"
    )
    credentials = urlunparse(segments)

    with NamedTemporaryFile(delete=True) as file:
        file.write(credentials.encode("utf-8"))
        file.flush()
        os.fsync(file)
        yield Path(file.name)
