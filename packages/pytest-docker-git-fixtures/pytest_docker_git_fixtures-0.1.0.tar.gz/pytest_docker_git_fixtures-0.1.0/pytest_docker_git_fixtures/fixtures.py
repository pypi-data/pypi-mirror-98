#!/usr/bin/env python

# pylint: disable=redefined-outer-name,too-many-arguments,too-many-locals

"""The actual fixtures, you found them ;)."""

import logging
import itertools

from base64 import b64encode
from functools import partial
from pathlib import Path
from ssl import create_default_context, SSLContext
from string import Template
from time import sleep, time
from typing import Dict, Generator, List, NamedTuple

import pytest

from lovely.pytest.docker.compose import Services
from _pytest.tmpdir import TempPathFactory

from .utils import (
    check_url_secure,
    DOCKER_GIT_SERVICE,
    DOCKER_GIT_SERVICE_PATTERN,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_user_defined_file,
    start_service,
)

# Caching is needed, as singular-fixtures and list-fixtures will conflict at scale_factor=1
# This appears to only matter when attempting to start the docker secure GIT service
# for the second time.
CACHE = {}

LOGGER = logging.getLogger(__name__)


class DockerGITCerts(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: Path
    ca_private_key: Path
    certificate: Path
    private_key: Path


class DockerGITInsecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    created_repos: List[str]
    docker_compose: Path
    endpoint: str
    mirrored_repos: List[str]
    service_name: str


# Note: NamedTuple does not support inheritance :(
class DockerGITSecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    auth_header: Dict[str, str]
    cacerts: Path
    certs: DockerGITCerts
    created_repos: List[str]
    docker_compose: Path
    endpoint: str
    htpasswd: Path
    mirrored_repos: List[str]
    password: str
    service_name: str
    ssl_context: SSLContext
    username: str


def _docker_compose_insecure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker GIT service.
    """
    cache_key = _docker_compose_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_GIT_SERVICE_PATTERN.format("insecure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            # TODO: lovely-docker-compose uses the file for teardown ...
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_compose_insecure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker GIT service.
    """
    for lst in _docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_compose_insecure_list(
    docker_compose_files: List[str],
    pdrf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker GIT service.
    """
    yield from _docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_compose_secure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker GIT
    service.
    """
    cache_key = _docker_compose_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_GIT_SERVICE_PATTERN.format("secure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_compose_secure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker GIT
    service.
    """
    for lst in _docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_compose_secure_list(
    docker_compose_files: List[str],
    pdrf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker GIT
    service.
    """
    yield from _docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_git_auth_header(
    *,
    docker_git_password_list: List[str],
    docker_git_username_list: List[str],
    scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker GIT service."""
    cache_key = _docker_git_auth_header.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        auth = b64encode(
            f"{docker_git_username_list[i]}:{docker_git_password_list[i]}".encode(
                "utf-8"
            )
        ).decode("utf-8")
        result.append({"Authorization": f"Basic {auth}"})
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_git_auth_header(
    docker_git_password: str, docker_git_username: str
) -> Dict[str, str]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker GIT service."""
    return _docker_git_auth_header(
        docker_git_password_list=[docker_git_password],
        docker_git_username_list=[docker_git_username],
        scale_factor=1,
    )[0]


@pytest.fixture(scope="session")
def docker_git_auth_header_list(
    docker_git_password_list: List[str],
    docker_git_username_list: List[str],
    pdrf_scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker GIT service."""
    return _docker_git_auth_header(
        docker_git_password_list=docker_git_password_list,
        docker_git_username_list=docker_git_username_list,
        scale_factor=pdrf_scale_factor,
    )


def _docker_git_cacerts(
    *,
    docker_git_certs_list: List[DockerGITCerts],
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    GIT service.
    """
    cache_key = _docker_git_cacerts.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "cacerts"),
            generate_cacerts(
                tmp_path_factory,
                certificate=docker_git_certs_list[i].ca_certificate,
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate cacerts!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_git_cacerts(
    docker_git_certs: DockerGITCerts,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    GIT service.
    """
    for lst in _docker_git_cacerts(
        docker_git_certs_list=[docker_git_certs],
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_git_cacerts_list(
    docker_git_certs_list: List[DockerGITCerts],
    pdrf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    GIT service.
    """
    yield from _docker_git_cacerts(
        docker_git_certs_list=docker_git_certs_list,
        pytestconfig=pytestconfig,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_git_certs(
    *, scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[DockerGITCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker GIT service."""
    # TODO: Augment to allow for reading certificates from /test ...
    cache_key = _docker_git_certs.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        tmp_path = tmp_path_factory.mktemp(__name__)
        keypair = generate_keypair()
        docker_git_cert = DockerGITCerts(
            ca_certificate=tmp_path.joinpath(f"{DOCKER_GIT_SERVICE}-ca-{i}.crt"),
            ca_private_key=tmp_path.joinpath(f"{DOCKER_GIT_SERVICE}-ca-{i}.key"),
            certificate=tmp_path.joinpath(f"{DOCKER_GIT_SERVICE}-{i}.crt"),
            private_key=tmp_path.joinpath(f"{DOCKER_GIT_SERVICE}-{i}.key"),
        )
        docker_git_cert.ca_certificate.write_bytes(keypair.ca_certificate)
        docker_git_cert.ca_private_key.write_bytes(keypair.ca_private_key)
        docker_git_cert.certificate.write_bytes(keypair.certificate)
        docker_git_cert.private_key.write_bytes(keypair.private_key)
        result.append(docker_git_cert)
    CACHE[cache_key] = result
    yield result
    for docker_git_cert in result:
        docker_git_cert.ca_certificate.unlink(missing_ok=True)
        docker_git_cert.ca_private_key.unlink(missing_ok=True)
        docker_git_cert.certificate.unlink(missing_ok=True)
        docker_git_cert.private_key.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def docker_git_certs(
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerGITCerts, None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker GIT service."""
    for lst in _docker_git_certs(scale_factor=1, tmp_path_factory=tmp_path_factory):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_git_certs_list(
    pdrf_scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[DockerGITCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker GIT service."""
    yield from _docker_git_certs(
        scale_factor=pdrf_scale_factor, tmp_path_factory=tmp_path_factory
    )


def _docker_git_htpasswd(
    *,
    docker_git_password_list: List[str],
    docker_git_username_list: List[str],
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure GIT service."""
    cache_key = _docker_git_htpasswd.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "htpasswd"),
            generate_htpasswd(
                tmp_path_factory,
                username=docker_git_username_list[i],
                password=docker_git_password_list[i],
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate htpasswd!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_git_htpasswd(
    docker_git_password: str,
    docker_git_username: str,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the htpasswd file for the secure GIT service."""
    for lst in _docker_git_htpasswd(
        docker_git_password_list=[docker_git_password],
        docker_git_username_list=[docker_git_username],
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_git_htpasswd_list(
    docker_git_password_list: List[str],
    docker_git_username_list: List[str],
    pdrf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure GIT service."""
    yield from _docker_git_htpasswd(
        docker_git_username_list=docker_git_username_list,
        docker_git_password_list=docker_git_password_list,
        pytestconfig=pytestconfig,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_git_insecure(
    *,
    docker_compose_insecure_list: List[Path],
    docker_services: Services,
    request,
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerGITInsecure], None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker GIT SCM."""
    cache_key = _docker_git_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_GIT_SERVICE_PATTERN.format("insecure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        create_repos = []
        mirror_repos = []
        if i == 0:
            LOGGER.debug("Initializing repositories in %s [%d] ...", service_name, i)
            create_repos = _get_create_repo(request)
            LOGGER.debug("  creating  :")
            for repo in create_repos:
                LOGGER.debug("    %s", repo)
            mirror_repos = _get_mirror_repo(request)
            LOGGER.debug("  mirroring :")
            for repo in mirror_repos:
                LOGGER.debug("    %s", repo)

        # Create a secure GIT service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_insecure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    # Note: Needed to correctly populate the embedded, consolidated, service template ...
                    "PATH_CERTIFICATE": "/dev/null",
                    "PATH_HTPASSWD": "/dev/null",
                    "PATH_KEY": "/dev/null",
                    "PDGF_CREATE_REPOS": ",".join(create_repos),
                    "PDGF_MIRROR_REPOS": ",".join(mirror_repos),
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting insecure docker GIT service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  service name   : %s", service_name)
        endpoint = start_service(
            docker_services,
            docker_compose=path_docker_compose,
            port=80,
            service_name=service_name,
        )
        LOGGER.debug("Insecure docker GIT endpoint [%d]: %s", i, endpoint)

        result.append(
            DockerGITInsecure(
                created_repos=create_repos,
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                mirrored_repos=mirror_repos,
                service_name=service_name,
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_git_insecure(
    docker_compose_insecure: Path,
    docker_services: Services,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerGITInsecure, None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker GIT SCM."""
    for lst in _docker_git_insecure(
        docker_compose_insecure_list=[docker_compose_insecure],
        docker_services=docker_services,
        request=request,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_git_insecure_list(
    docker_compose_insecure_list: List[Path],
    docker_services: Services,
    pdrf_scale_factor: int,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerGITInsecure], None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker GIT SCM."""
    yield from _docker_git_insecure(
        docker_compose_insecure_list=docker_compose_insecure_list,
        docker_services=docker_services,
        request=request,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_git_password(*, scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure GIT service."""
    cache_key = _docker_git_password.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.password.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_git_password() -> str:
    """Provides the password to use for authentication to the secure GIT service."""
    return _docker_git_password(scale_factor=1)[0]


@pytest.fixture(scope="session")
def docker_git_password_list(pdrf_scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure GIT service."""
    return _docker_git_password(scale_factor=pdrf_scale_factor)


def _docker_git_secure(
    *,
    docker_compose_secure_list: List[Path],
    docker_git_auth_header_list: List[Dict[str, str]],
    docker_git_cacerts_list: List[Path],
    docker_git_certs_list: List[DockerGITCerts],
    docker_git_htpasswd_list: List[Path],
    docker_git_password_list: List[str],
    docker_git_ssl_context_list: List[SSLContext],
    docker_git_username_list: List[str],
    docker_services: Services,
    request,
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerGITSecure], None, None]:
    """Provides the endpoint of a local, mutable, secure, docker GIT SCM."""
    cache_key = _docker_git_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_GIT_SERVICE_PATTERN.format("secure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        create_repos = []
        mirror_repos = []
        if i == 0:
            create_repos = _get_create_repo(request)
            LOGGER.debug("  creating  :")
            for repo in create_repos:
                LOGGER.debug("    %s", repo)
            mirror_repos = _get_mirror_repo(request)
            LOGGER.debug("  mirroring :")
            for repo in mirror_repos:
                LOGGER.debug("    %s", repo)

        # Create a secure GIT service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_secure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    "PATH_CERTIFICATE": docker_git_certs_list[i].certificate,
                    "PATH_HTPASSWD": docker_git_htpasswd_list[i],
                    "PATH_KEY": docker_git_certs_list[i].private_key,
                    "PDGF_CREATE_REPOS": ",".join(create_repos),
                    "PDGF_MIRROR_REPOS": ",".join(mirror_repos),
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting secure docker GIT service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  ca certificate : %s", docker_git_certs_list[i].ca_certificate)
        LOGGER.debug("  certificate    : %s", docker_git_certs_list[i].certificate)
        LOGGER.debug("  htpasswd       : %s", docker_git_htpasswd_list[i])
        LOGGER.debug("  private key    : %s", docker_git_certs_list[i].private_key)
        LOGGER.debug("  password       : %s", docker_git_password_list[i])
        LOGGER.debug("  service name   : %s", service_name)
        LOGGER.debug("  username       : %s", docker_git_username_list[i])

        check_server = partial(
            check_url_secure,
            auth_header=docker_git_auth_header_list[i],
            ssl_context=docker_git_ssl_context_list[i],
        )
        endpoint = start_service(
            docker_services,
            check_server=check_server,
            docker_compose=path_docker_compose,
            port=443,
            service_name=service_name,
        )
        LOGGER.debug("Secure docker GIT endpoint [%d]: %s", i, endpoint)

        result.append(
            DockerGITSecure(
                auth_header=docker_git_auth_header_list[i],
                cacerts=docker_git_cacerts_list[i],
                certs=docker_git_certs_list[i],
                created_repos=create_repos,
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                htpasswd=docker_git_htpasswd_list[i],
                mirrored_repos=mirror_repos,
                password=docker_git_password_list[i],
                service_name=service_name,
                ssl_context=docker_git_ssl_context_list[i],
                username=docker_git_username_list[i],
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_git_secure(
    docker_compose_secure: Path,
    docker_git_auth_header: Dict[str, str],
    docker_git_cacerts: Path,
    docker_git_certs: DockerGITCerts,
    docker_git_htpasswd: Path,
    docker_git_password: str,
    docker_git_ssl_context: SSLContext,
    docker_git_username: str,
    docker_services: Services,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerGITSecure, None, None]:
    """Provides the endpoint of a local, mutable, secure, docker GIT SCM."""
    for lst in _docker_git_secure(
        docker_compose_secure_list=[docker_compose_secure],
        docker_git_auth_header_list=[docker_git_auth_header],
        docker_git_cacerts_list=[docker_git_cacerts],
        docker_git_certs_list=[docker_git_certs],
        docker_git_htpasswd_list=[docker_git_htpasswd],
        docker_git_password_list=[docker_git_password],
        docker_git_ssl_context_list=[docker_git_ssl_context],
        docker_git_username_list=[docker_git_username],
        docker_services=docker_services,
        request=request,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_git_secure_list(
    docker_compose_secure_list: List[Path],
    docker_git_auth_header_list: List[Dict[str, str]],
    docker_git_cacerts_list: List[Path],
    docker_git_certs_list: List[DockerGITCerts],
    docker_git_htpasswd_list: List[Path],
    docker_git_password_list: List[str],
    docker_git_ssl_context_list: List[SSLContext],
    docker_git_username_list: List[str],
    docker_services: Services,
    pdrf_scale_factor: int,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerGITSecure], None, None]:
    """Provides the endpoint of a local, mutable, secure, docker GIT SCM."""
    yield from _docker_git_secure(
        docker_compose_secure_list=docker_compose_secure_list,
        docker_git_auth_header_list=docker_git_auth_header_list,
        docker_git_cacerts_list=docker_git_cacerts_list,
        docker_git_certs_list=docker_git_certs_list,
        docker_git_htpasswd_list=docker_git_htpasswd_list,
        docker_git_password_list=docker_git_password_list,
        docker_git_ssl_context_list=docker_git_ssl_context_list,
        docker_git_username_list=docker_git_username_list,
        docker_services=docker_services,
        scale_factor=pdrf_scale_factor,
        request=request,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_git_ssl_context(
    *, docker_git_cacerts_list: List[Path], scale_factor: int
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker GIT service.
    """
    cache_key = _docker_git_ssl_context.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(create_default_context(cafile=str(docker_git_cacerts_list[i])))
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_git_ssl_context(docker_git_cacerts: Path) -> SSLContext:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker GIT service.
    """
    return _docker_git_ssl_context(
        docker_git_cacerts_list=[docker_git_cacerts], scale_factor=1
    )[0]


@pytest.fixture(scope="session")
def docker_git_ssl_context_list(
    docker_git_cacerts_list: List[Path],
    pdrf_scale_factor: int,
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker GIT service.
    """
    return _docker_git_ssl_context(
        docker_git_cacerts_list=docker_git_cacerts_list,
        scale_factor=pdrf_scale_factor,
    )


def _docker_git_username(*, scale_factor: int) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure GIT service."""
    cache_key = _docker_git_username.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.username.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_git_username() -> str:
    """Retrieve the name of the user to use for authentication to the secure GIT service."""
    return _docker_git_username(scale_factor=1)[0]


@pytest.fixture(scope="session")
def docker_git_username_list(
    pdrf_scale_factor: int,
) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure GIT service."""
    return _docker_git_username(scale_factor=pdrf_scale_factor)


@pytest.fixture(scope="session")
def pdrf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 1


def _get_create_repo(request) -> List[str]:
    """
    Retrieves the list of all GIT repositories to be created.

    Args:
        request: The pytest requests object from which to retrieve the marks.

    Returns: The list of GIT repositories to be created.
    """
    names = request.config.getoption("--create-repo", [])
    # names.extend(request.node.get_closest_marker("create_repo", []))

    # * Split ',' separated lists
    # * Remove duplicates - see conftest.py::pytest_collection_modifyitems()
    names = [name for i in names for name in i.split(",")]
    return list(set(names))


def _get_mirror_repo(request) -> List[str]:
    """
    Retrieves the list of all GIT repositories to be mirrored.

    Args:
        request: The pytest requests object from which to retrieve the marks.

    Returns: The list of GIT repositories to be mirrored.
    """
    uris = request.config.getoption("--mirror-repo", [])
    # uris.extend(request.node.get_closest_marker("mirror_repo", []))

    # * Split ',' separated lists
    # * Remove duplicates - see conftest.py::pytest_collection_modifyitems()
    uris = [uri for i in uris for uri in i.split(",")]
    return list(set(uris))
