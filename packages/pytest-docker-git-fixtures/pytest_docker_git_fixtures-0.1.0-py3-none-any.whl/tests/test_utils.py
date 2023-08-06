#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging

from pathlib import Path
from time import time
from typing import List

from OpenSSL import crypto
from _pytest.tmpdir import TempPathFactory

from pytest_docker_git_fixtures import (
    DOCKER_GIT_SERVICE_PATTERN,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_created_repos,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_mirrored_repos,
    get_user_defined_file,
)
from pytest_docker_git_fixtures.utils import git_askpass_script, git_credentials_store

LOGGER = logging.getLogger(__name__)


# TODO: test_check_url_secure


def test_generate_cacerts(tmp_path_factory: TempPathFactory, tmp_path: Path):
    """Test that a temporary cacerts file can be generated."""
    certificate = "MY CERTIFICATE VALUE"
    path = tmp_path.joinpath("certificate")
    path.write_text(certificate, "utf-8")
    path_last = None
    for path in generate_cacerts(tmp_path_factory, certificate=path):
        assert path.exists()
        content = path.read_text("utf-8")
        assert certificate in content
        path_last = path
    assert path_last
    assert not path_last.exists()


def test_generate_htpasswd(tmp_path_factory: TempPathFactory):
    """Test that a temporary htpasswd file can be generated."""
    username = "myusername"
    password = "mypassword"
    path_last = None
    for path in generate_htpasswd(
        tmp_path_factory, password=password, username=username
    ):
        assert path.exists()
        content = path.read_text("utf-8")
        assert username in content
        assert password not in content
        path_last = path
    assert path_last
    assert not path_last.exists()


def test_generate_keypair():
    """Test that a keypair can be generated."""
    keypair = generate_keypair()
    assert keypair.ca_certificate
    assert keypair.ca_private_key
    assert keypair.certificate
    assert keypair.private_key

    x509_store = crypto.X509Store()
    ca_certificate = crypto.load_certificate(
        crypto.FILETYPE_PEM, keypair.ca_certificate
    )
    x509_store.add_cert(ca_certificate)

    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, keypair.certificate)
    x509_store_context = crypto.X509StoreContext(x509_store, certificate)
    x509_store_context.verify_certificate()


def test_get_created_repos_empty(request):
    """Tests that 'create_repo' pytest marks can be retrieved."""

    assert not get_created_repos(request)


def test_get_docker_compose_user_defined(docker_compose_files: List[str]):
    """Tests that the user defined check fails here."""

    service_name = DOCKER_GIT_SERVICE_PATTERN.format("insecure", 0)
    for _ in get_docker_compose_user_defined(docker_compose_files, service_name):
        assert False
    service_name = DOCKER_GIT_SERVICE_PATTERN.format("secure", 0)
    for _ in get_docker_compose_user_defined(docker_compose_files, service_name):
        assert False


def test_get_embedded_file(tmp_path_factory: TempPathFactory):
    """Test that an embedded file can be replicated to a temporary file."""
    path_last = None
    for path in get_embedded_file(tmp_path_factory, name="docker-compose.yml"):
        assert path.exists()
        content = path.read_text("utf-8")
        assert "git" in content
        path_last = path
    assert path_last
    assert not path_last.exists()


def test_get_mirrored_repos_empty(request):
    """Tests that 'mirror_repo' pytest marks can be retrieved."""

    assert not get_mirrored_repos(request)


def test_get_user_defined_file(pytestconfig: "_pytest.config.Config"):
    """Tests that the user defined check fails here."""

    for _ in get_user_defined_file(pytestconfig, "does_not_exist"):
        assert False


# TODO: test_start_service


def test_git_askpass_script(tmp_path_factory: TempPathFactory):
    """Test that a git askpass script can be initialized."""
    password = f"password-{time()}"
    path = None
    with git_askpass_script(tmp_path_factory, password=password) as askpass_script:
        path = askpass_script
        assert path.exists()
        result = path.read_text("utf-8")
        assert password in result
    assert not path.exists()


def test_git_credentials_store():
    """Test that a git credentials store can be initialized."""
    endpoint = f"base64_{time()}"
    password = f"password-{time()}"
    uri = f"git://{endpoint}/suffix"
    username = f"username-{time()}"
    path = None
    with git_credentials_store(
        password=password, uri=uri, username=username
    ) as credentials_store:
        path = credentials_store
        assert path.exists()
        result = path.read_text("utf-8")
        assert result == f"git://{username}:{password}@{endpoint}/suffix"
    assert not path.exists()
