#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging
import subprocess

from base64 import b64decode
from pathlib import Path
from ssl import SSLContext
from time import time
from typing import Dict, List

import pytest
import requests

from _pytest.tmpdir import TempPathFactory

from pytest_docker_git_fixtures import (
    DockerGITCerts,
    DockerGITInsecure,
    DockerGITSecure,
    DOCKER_GIT_SERVICE_PATTERN,
)
from pytest_docker_git_fixtures.fixtures import _get_create_repo, _get_mirror_repo
from pytest_docker_git_fixtures.utils import git_askpass_script

LOGGER = logging.getLogger(__name__)


# Override fixture for testing
@pytest.fixture(scope="session")
def pdrf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 4


def no_duplicates(lst: List) -> bool:
    """Tests if a list contains duplicate values."""
    return len(lst) == len(set(lst))


def test_docker_compose_insecure(docker_compose_insecure: Path):
    """Test that the embedded docker-compose for insecure scms can be copied to a temporary file."""
    service_name = DOCKER_GIT_SERVICE_PATTERN.format("insecure", 0)
    assert service_name in docker_compose_insecure.read_text()


def test_docker_compose_insecure_list(
    docker_compose_insecure_list: List[Path], pdrf_scale_factor: int
):
    """Test that the embedded docker-compose for insecure scms can be copied to a temporary file."""
    for i in range(pdrf_scale_factor):
        service_name = DOCKER_GIT_SERVICE_PATTERN.format("insecure", i)
        assert service_name in docker_compose_insecure_list[i].read_text()
    assert no_duplicates(docker_compose_insecure_list)


def test_docker_compose_secure(docker_compose_secure: Path):
    """Test that the embedded docker-compose for secure scms can be copied to a temporary file."""
    service_name = DOCKER_GIT_SERVICE_PATTERN.format("secure", 0)
    assert service_name in docker_compose_secure.read_text()


def test_docker_compose_secure_list(
    docker_compose_secure_list: List[Path], pdrf_scale_factor: int
):
    """Test that the embedded docker-compose for secure scms can be copied to a temporary file."""
    for i in range(pdrf_scale_factor):
        service_name = DOCKER_GIT_SERVICE_PATTERN.format("secure", i)
        assert service_name in docker_compose_secure_list[i].read_text()
    assert no_duplicates(docker_compose_secure_list)


def test_docker_git_auth_header(
    docker_git_auth_header: Dict[str, str],
    docker_git_password: str,
    docker_git_username: str,
):
    """Test that an HTTP basic authentication header can be provided."""
    assert "Authorization" in docker_git_auth_header
    string = b64decode(
        docker_git_auth_header["Authorization"].split()[1].encode("utf-8")
    ).decode("utf-8")
    assert docker_git_password in string
    assert docker_git_username in string


def test_docker_git_auth_header_list(
    docker_git_auth_header_list: List[Dict[str, str]],
    docker_git_password_list: List[str],
    docker_git_username_list: List[str],
    pdrf_scale_factor: int,
):
    """Test that an HTTP basic authentication header can be provided."""
    for i in range(pdrf_scale_factor):
        assert "Authorization" in docker_git_auth_header_list[i]
        string = b64decode(
            docker_git_auth_header_list[i]["Authorization"].split()[1].encode("utf-8")
        ).decode("utf-8")
        assert docker_git_password_list[i] in string
        assert docker_git_username_list[i] in string
    assert no_duplicates([str(i) for i in docker_git_auth_header_list])
    assert no_duplicates(docker_git_password_list)
    assert no_duplicates(docker_git_username_list)


def test_docker_git_cacerts(docker_git_cacerts: Path, docker_git_certs: DockerGITCerts):
    """Test that a temporary CA certificate trust store can be provided."""
    assert docker_git_cacerts.exists()
    cacerts = docker_git_cacerts.read_text("utf-8")

    ca_cert = docker_git_certs.ca_certificate.read_text("utf-8")
    assert ca_cert in cacerts

    ca_key = docker_git_certs.ca_private_key.read_text("utf-8")
    assert ca_key not in cacerts

    cert = docker_git_certs.certificate.read_text("utf-8")
    assert cert not in cacerts

    key = docker_git_certs.private_key.read_text("utf-8")
    assert key not in cacerts


def test_docker_git_cacerts_list(
    docker_git_cacerts_list: List[Path],
    docker_git_certs_list: List[DockerGITCerts],
    pdrf_scale_factor: int,
):
    """Test that a temporary CA certificate trust store can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_git_cacerts_list[i].exists()
        cacerts = docker_git_cacerts_list[i].read_text("utf-8")

        ca_cert = docker_git_certs_list[i].ca_certificate.read_text("utf-8")
        assert ca_cert in cacerts

        ca_key = docker_git_certs_list[i].ca_private_key.read_text("utf-8")
        assert ca_key not in cacerts

        cert = docker_git_certs_list[i].certificate.read_text("utf-8")
        assert cert not in cacerts

        key = docker_git_certs_list[i].private_key.read_text("utf-8")
        assert key not in cacerts
    assert no_duplicates(docker_git_cacerts_list)
    assert no_duplicates(docker_git_certs_list)


def test_docker_git_certs(docker_git_certs: DockerGITCerts):
    """Test that a certificate and private key can be provided."""
    assert docker_git_certs.ca_certificate.exists()
    assert "BEGIN CERTIFICATE" in docker_git_certs.ca_certificate.read_text("utf-8")
    assert docker_git_certs.ca_private_key.exists()
    assert "BEGIN PRIVATE KEY" in docker_git_certs.ca_private_key.read_text("utf-8")
    assert docker_git_certs.certificate.exists()
    assert "BEGIN CERTIFICATE" in docker_git_certs.certificate.read_text("utf-8")
    assert docker_git_certs.private_key.exists()
    assert "BEGIN PRIVATE KEY" in docker_git_certs.private_key.read_text("utf-8")


def test_docker_git_certs_list(
    docker_git_certs_list: List[DockerGITCerts], pdrf_scale_factor: int
):
    """Test that a certificate and private key can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_git_certs_list[i].ca_certificate.exists()
        assert "BEGIN CERTIFICATE" in docker_git_certs_list[i].ca_certificate.read_text(
            "utf-8"
        )
        assert docker_git_certs_list[i].ca_private_key.exists()
        assert "BEGIN PRIVATE KEY" in docker_git_certs_list[i].ca_private_key.read_text(
            "utf-8"
        )
        assert docker_git_certs_list[i].certificate.exists()
        assert "BEGIN CERTIFICATE" in docker_git_certs_list[i].certificate.read_text(
            "utf-8"
        )
        assert docker_git_certs_list[i].private_key.exists()
        assert "BEGIN PRIVATE KEY" in docker_git_certs_list[i].private_key.read_text(
            "utf-8"
        )
    assert no_duplicates(docker_git_certs_list)


def test_docker_git_htpasswd(
    docker_git_htpasswd: Path,
    docker_git_password: str,
    docker_git_username: str,
):
    """Test that a htpasswd can be provided."""
    assert docker_git_htpasswd.exists()
    content = docker_git_htpasswd.read_text("utf-8")
    assert docker_git_username in content
    assert docker_git_password not in content


def test_docker_git_htpasswd_list(
    docker_git_htpasswd_list: List[Path],
    docker_git_password_list: List[str],
    docker_git_username_list: List[str],
    pdrf_scale_factor: int,
):
    """Test that a htpasswd can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_git_htpasswd_list[i].exists()
        content = docker_git_htpasswd_list[i].read_text("utf-8")
        assert docker_git_username_list[i] in content
        assert docker_git_password_list[i] not in content
    assert no_duplicates(docker_git_htpasswd_list)
    assert no_duplicates(docker_git_password_list)
    assert no_duplicates(docker_git_username_list)


@pytest.mark.create_repo("test_docker_git_insecure")
@pytest.mark.mirror_repo("https://github.com/crashvb/shim-bind.git")
def test_docker_git_insecure(docker_git_insecure: DockerGITInsecure, tmp_path: Path):
    """Test that an insecure docker git can be instantiated."""
    assert "127.0.0.1" in docker_git_insecure.endpoint

    uri_insecure = f"http://{docker_git_insecure.endpoint}/insecure/shim-bind.git"
    uri_secure = f"http://{docker_git_insecure.endpoint}/secure/shim-bind.git"

    # Should not be able to clone from secure w/o credentials ...
    path = tmp_path.joinpath(f"cloned-repo-{time()}")
    with pytest.raises(subprocess.CalledProcessError) as exception:
        subprocess.run(
            ["git", "clone", uri_secure, str(path)],
            check=True,
            cwd=str(tmp_path),
            env={"GIT_TERMINAL_PROMPT": "0"},
            stderr=subprocess.STDOUT,
        )
    assert "returned non-zero exit status" in str(exception.value)
    assert not path.exists()

    # Should be able to clone from insecure w/o credentials ...
    path = tmp_path.joinpath(f"cloned-repo-{time()}")
    subprocess.run(
        ["git", "clone", uri_insecure, str(path)],
        check=True,
        cwd=str(tmp_path),
        stderr=subprocess.STDOUT,
    )
    assert path.joinpath("README.md").exists()

    # Should not be able to push to insecure w/o credentials ...
    with pytest.raises(subprocess.CalledProcessError) as exception:
        subprocess.run(
            ["git", "push", uri_insecure, "master"],
            check=True,
            cwd=str(path),
            env={"GIT_TERMINAL_PROMPT": "0"},
            stderr=subprocess.STDOUT,
        )
    assert "returned non-zero exit status" in str(exception.value)

    # Should not be able to push to secure w/o credentials ...
    with pytest.raises(subprocess.CalledProcessError) as exception:
        subprocess.run(
            ["git", "push", uri_secure, "master"],
            check=True,
            cwd=str(path),
            env={"GIT_TERMINAL_PROMPT": "0"},
            stderr=subprocess.STDOUT,
        )
    assert "returned non-zero exit status" in str(exception.value)


@pytest.mark.online
def test_docker_git_insecure_list(
    docker_git_insecure_list: List[DockerGITInsecure],
    pdrf_scale_factor: int,
    tmp_path: Path,
):
    """Test that an insecure docker git can be instantiated."""
    for i in range(pdrf_scale_factor):
        assert "127.0.0.1" in docker_git_insecure_list[i].endpoint

        # Default listener ...
        response = requests.get(f"http://{docker_git_insecure_list[i].endpoint}/")
        assert response.status_code == 200
        assert response.content == b"pytest-docker-git-fixtures-docker\n"

        if i > 0:
            continue

        uri_insecure = (
            f"http://{docker_git_insecure_list[i].endpoint}/insecure/shim-bind.git"
        )
        uri_secure = (
            f"http://{docker_git_insecure_list[i].endpoint}/secure/shim-bind.git"
        )

        # Should not be able to clone from secure w/o credentials ...
        path = tmp_path.joinpath(f"cloned-repo-{time()}")
        with pytest.raises(subprocess.CalledProcessError) as exception:
            subprocess.run(
                ["git", "clone", uri_secure, str(path)],
                check=True,
                cwd=str(tmp_path),
                env={"GIT_TERMINAL_PROMPT": "0"},
                stderr=subprocess.STDOUT,
            )
        assert "returned non-zero exit status" in str(exception.value)
        assert not path.exists()

        # Should be able to clone from insecure w/o credentials ...
        path = tmp_path.joinpath(f"cloned-repo-{time()}")
        subprocess.run(
            ["git", "clone", uri_insecure, str(path)],
            check=True,
            cwd=str(tmp_path),
            stderr=subprocess.STDOUT,
        )
        assert path.joinpath("README.md").exists()

        # Should not be able to push to insecure ...
        with pytest.raises(subprocess.CalledProcessError) as exception:
            subprocess.run(
                ["git", "push", uri_insecure, "master"],
                check=True,
                cwd=str(path),
                env={"GIT_TERMINAL_PROMPT": "0"},
                stderr=subprocess.STDOUT,
            )
        assert "returned non-zero exit status" in str(exception.value)

        # Should not be able to push to secure ...
        with pytest.raises(subprocess.CalledProcessError) as exception:
            subprocess.run(
                ["git", "push", uri_secure, "master"],
                check=True,
                cwd=str(path),
                env={"GIT_TERMINAL_PROMPT": "0"},
                stderr=subprocess.STDOUT,
            )
        assert "returned non-zero exit status" in str(exception.value)
    assert no_duplicates([str(i) for i in docker_git_insecure_list])


def test_docker_git_password(docker_git_password: str):
    """Test that a password can be provided."""
    assert docker_git_password


def test_docker_git_password_list(
    docker_git_password_list: List[str], pdrf_scale_factor: int
):
    """Test that a password can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_git_password_list[i]
    assert no_duplicates(docker_git_password_list)


@pytest.mark.create_repo("test_docker_git_secure")
@pytest.mark.mirror_repo("https://github.com/crashvb/scratch-docker.git")
def test_docker_git_secure(
    docker_git_secure: DockerGITSecure,
    tmp_path: Path,
    tmp_path_factory: TempPathFactory,
):
    """Test that an secure docker git can be instantiated."""
    assert "127.0.0.1" in docker_git_secure.endpoint

    uri_insecure = f"https://{docker_git_secure.endpoint}/insecure/scratch-docker.git"
    uri_secure = f"https://{docker_git_secure.endpoint}/secure/scratch-docker.git"

    # Should be able to clone from insecure w/o credentials ...
    path = tmp_path.joinpath(f"cloned-repo-{time()}")
    subprocess.run(
        [
            "git",
            "-c",
            f"http.sslCAinfo={docker_git_secure.cacerts}",
            "clone",
            uri_insecure,
            str(path),
        ],
        check=True,
        cwd=str(tmp_path),
        stderr=subprocess.STDOUT,
    )
    assert path.joinpath("README.md").exists()

    # Should not be able to clone from secure w/o credentials ...
    path = tmp_path.joinpath(f"cloned-repo-{time()}")
    with pytest.raises(subprocess.CalledProcessError) as exception:
        subprocess.run(
            [
                "git",
                "-c",
                f"http.sslCAinfo={docker_git_secure.cacerts}",
                "clone",
                uri_secure,
                str(path),
            ],
            check=True,
            cwd=str(tmp_path),
            env={"GIT_TERMINAL_PROMPT": "0"},
            stderr=subprocess.STDOUT,
        )
    assert "returned non-zero exit status" in str(exception.value)
    assert not path.exists()

    uri_secure = f"https://{docker_git_secure.username}@{docker_git_secure.endpoint}/secure/scratch-docker.git"

    # Should be able to clone from secure w/ credentials ...
    path = tmp_path.joinpath(f"cloned-repo-{time()}")
    with git_askpass_script(
        tmp_path_factory, password=docker_git_secure.password
    ) as askpass_script:
        subprocess.run(
            ["git", "clone", uri_secure, str(path)],
            check=True,
            cwd=str(tmp_path),
            env={
                "GIT_ASKPASS": str(askpass_script),
                "GIT_SSL_CAINFO": docker_git_secure.cacerts,
                "GIT_TERMINAL_PROMPT": "0",
            },
            stderr=subprocess.STDOUT,
        )
        assert path.joinpath("README.md").exists()

        # TODO: Do we really need to test insecure variant of push here?

        # Should be able to push to secure w/ credentials ...
        subprocess.run(
            ["git", "push", uri_secure, "master"],
            check=True,
            cwd=str(path),
            env={
                "GIT_ASKPASS": str(askpass_script),
                "GIT_SSL_CAINFO": docker_git_secure.cacerts,
                "GIT_TERMINAL_PROMPT": "0",
            },
            stderr=subprocess.STDOUT,
        )


@pytest.mark.online
def test_docker_git_secure_list(
    docker_git_secure_list: List[DockerGITSecure],
    pdrf_scale_factor: int,
    tmp_path: Path,
    tmp_path_factory: TempPathFactory,
):
    """Test that an secure docker git can be instantiated."""
    for i in range(pdrf_scale_factor):
        assert "127.0.0.1" in docker_git_secure_list[i].endpoint

        # Default listener ...
        response = requests.get(
            f"https://{docker_git_secure_list[i].endpoint}/",
            headers=docker_git_secure_list[i].auth_header,
            verify=str(docker_git_secure_list[i].cacerts),
        )
        assert response.status_code == 200
        assert response.content == b"pytest-docker-git-fixtures-docker\n"

        if i > 0:
            continue

        uri_insecure = (
            f"https://{docker_git_secure_list[i].endpoint}/insecure/scratch-docker.git"
        )
        uri_secure = (
            f"https://{docker_git_secure_list[i].endpoint}/secure/scratch-docker.git"
        )

        # Should be able to clone from insecure w/o credentials ...
        path = tmp_path.joinpath(f"cloned-repo-{time()}")
        subprocess.run(
            [
                "git",
                "-c",
                f"http.sslCAinfo={docker_git_secure_list[i].cacerts}",
                "clone",
                uri_insecure,
                str(path),
            ],
            check=True,
            cwd=str(tmp_path),
            stderr=subprocess.STDOUT,
        )
        assert path.joinpath("README.md").exists()

        # Should not be able to clone from secure w/o credentials ...
        path = tmp_path.joinpath(f"cloned-repo-{time()}")
        with pytest.raises(subprocess.CalledProcessError) as exception:
            subprocess.run(
                [
                    "git",
                    "-c",
                    f"http.sslCAinfo={docker_git_secure_list[i].cacerts}",
                    "clone",
                    uri_secure,
                    str(path),
                ],
                check=True,
                cwd=str(tmp_path),
                env={"GIT_TERMINAL_PROMPT": "0"},
                stderr=subprocess.STDOUT,
            )
        assert "returned non-zero exit status" in str(exception.value)
        assert not path.exists()

        uri_secure = (
            f"https://{docker_git_secure_list[i].username}@"
            f"{docker_git_secure_list[i].endpoint}/secure/scratch-docker.git"
        )

        # Should be able to clone from secure w/ credentials ...
        path = tmp_path.joinpath(f"cloned-repo-{time()}")
        with git_askpass_script(
            tmp_path_factory, password=docker_git_secure_list[i].password
        ) as askpass_script:
            subprocess.run(
                ["git", "clone", uri_secure, str(path)],
                check=True,
                cwd=str(tmp_path),
                env={
                    "GIT_ASKPASS": str(askpass_script),
                    "GIT_SSL_CAINFO": docker_git_secure_list[i].cacerts,
                    "GIT_TERMINAL_PROMPT": "0",
                },
                stderr=subprocess.STDOUT,
            )
            assert path.joinpath("README.md").exists()

            # TODO: Do we really need to test insecure variant of push here?

            # Should be able to push to secure w/ credentials ...
            subprocess.run(
                ["git", "push", uri_secure, "master"],
                check=True,
                cwd=str(path),
                env={
                    "GIT_ASKPASS": str(askpass_script),
                    "GIT_SSL_CAINFO": docker_git_secure_list[i].cacerts,
                    "GIT_TERMINAL_PROMPT": "0",
                },
                stderr=subprocess.STDOUT,
            )


def test_docker_git_ssl_context(docker_git_ssl_context: SSLContext):
    """Test that an ssl context can be provided."""
    assert isinstance(docker_git_ssl_context, SSLContext)


def test_docker_git_ssl_context_list(
    docker_git_ssl_context_list: List[SSLContext], pdrf_scale_factor: int
):
    """Test that an ssl context can be provided."""
    for i in range(pdrf_scale_factor):
        assert isinstance(docker_git_ssl_context_list[i], SSLContext)
    assert no_duplicates(docker_git_ssl_context_list)


def test_docker_git_username(docker_git_username: str):
    """Test that a username can be provided."""
    assert docker_git_username


def test_docker_git_username_list(
    docker_git_username_list: List[str], pdrf_scale_factor: int
):
    """Test that a username can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_git_username_list[i]
    assert no_duplicates(docker_git_username_list)


def test__get_create_repo(request):
    """Test that a marks can be retrieved."""
    marks = _get_create_repo(request)
    assert marks
    assert (
        marks.sort()
        == [
            "test_docker_git_insecure",
            "test_docker_git_secure",
        ].sort()
    )


def test__get_mirror_repo(request):
    """Test that a marks can be retrieved."""
    marks = _get_mirror_repo(request)
    assert marks
    assert (
        marks.sort()
        == [
            "https://github.com/crashvb/scratch-docker.git",
            "https://github.com/crashvb/shim-bind.git",
        ].sort()
    )
