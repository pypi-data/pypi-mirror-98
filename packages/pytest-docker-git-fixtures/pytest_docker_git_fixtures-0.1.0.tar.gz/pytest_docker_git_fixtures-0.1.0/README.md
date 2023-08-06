# pytest-docker-git-fixtures

## Overview

Pytest fixtures to instantiate and populated local docker GIT SCMs, using [lovely-pytest-docker](https://pypi.org/project/lovely-pytest-docker), for testing.

## Getting Started

Update <tt>setup.py</tt> to include:

```python
from distutils.core import setup

setup(
	tests_require=["pytest-docker-git-fixtures"]
)
```

All fixtures should be automatically included via the <tt>pytest11</tt> entry point.
```python
import pytest
import subprocess
from pathlib import Path
from pytest_docker_git_fixtures import DockerGITInsecure, DockerGITSecure  # Optional, for typing

@pytest.mark.create_repo("test_docker_git_secure")
@pytest.mark.mirror_repo("https://github.com/crashvb/shim-bind.git")
def test_docker_git_secure(docker_git_secure: DockerGITSecure, tmp_path: Path):
    uri = f"https://{docker_git_secure.endpoint}/secure/shim-bind.git"
    path = tmp_path.join("local-clone")
    subprocess.run(
        ["git", "clone", uri, str(path)],
        check=True,
        cwd=str(tmp_path),
        stderr=subprocess.STDOUT,
    )
    assert path.joinpath("README.md").exists()

@pytest.mark.create_repo("test_docker_git_insecure")
def test_docker_git_insecure(docker_git_insecure: DockerGITInsecure, tmp_path: Path):
    uri = f"https://{docker_git_insecure.endpoint}/insecure/test_docker_git_insecure.git"
    path = tmp_path.join("local-clone")
    subprocess.run(
        ["git", "clone", uri, str(path)],
        check=True,
        cwd=str(tmp_path),
        stderr=subprocess.STDOUT,
    )
    assert path.exists()
```

The `create_repo` and `mirror_repo` marks can optionally be added to stage repositories in the GIT prior to testing. See [Markers](#markers) for details.
## Compatibility

* Tested with python 3.8

## Installation
### From [pypi.org](https://pypi.org/project/pytest-docker-git-fixtures/)

```
$ pip install pytest_docker_git_fixtures
```

### From source code

```bash
$ git clone https://github.com/crashvb/pytest-docker-git-fixtures
$ cd pytest-docker-git-fixtures
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## <a name="fixtures"></a>Fixtures

### <a name="docker_compose_insecure"></a> docker_compose_insecure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-git-insecure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the insecure docker GIT service.

### <a name="docker_compose_secure"></a> docker_compose_secure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-git-secure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the secure docker GIT service; however, unlike the configuration returned by the [docker_compose_insecure](#docker_compose_insecure) fixture, this configuration will be treated as a template; the <tt>$PATH_CERTIFICATE</tt>, <tt>$PATH_HTPASSWD</tt>, and <tt>$PATH_KEY</tt> tokens will be populated with the absolute paths provided by the [docker_git_certs](#docker_git_certs) and [docker_git_htpasswd](#docker_git_htpasswd) fixtures, as appropriate.

### <a name="docker_git_auth_header"></a> docker_git_auth_header

Retrieves an HTTP basic authentication header that is populated with credentials that can access the secure docker GIT service. The credentials are retrieved from the [docker_git_password](#docker_git_password) and [docker_git_username](#docker_git_username) fixtures.

### <a name="docker_git_cacerts"></a> docker_git_cacerts

Locates a user-defined CA trust store (<tt>tests/cacerts</tt>) to use to verify connections to the secure docker GIT service. If one cannot be located, a temporary trust store is created containing certificates from <tt>certifi</tt> and the [docker_git_certs](#docker_git_certs) fixture. This fixture is used to instantiate the secure docker GIT service.

### <a name="docker_git_certs"></a> docker_git_certs

Returns the paths of the self-signed certificate authority certificate, certificate, and private key that are used by the secure docker GIT service. This fixture is used to instantiate the secure docker GIT service.

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **ca_certificate** - Path to the self-signed certificate authority certificate.
* **ca_private_key** - Path to the self-signed certificate authority private key.
* **certificate** - Path to the certificate.
* **private_key** - Path to the private key.

Typing is provided by `pytest_docker_git_fixtures.DockerGITCerts`.

### <a name="docker_git_hwpasswd"></a> docker_git_htpasswd

Provides the path to a htpasswd file that is used by the secure docker GIT service. If a user-defined htpasswd file (<tt>tests/htpasswd</tt>) can be located, it is used. Otherwise, a temporary htpasswd file is created using credentials from the [docker_git_password](#docker_git_password) and [docker_git_username](#docker_git_username) fixtures. This fixture is used to instantiate the secure docker GIT service.

### <a name="docker_git_insecure"></a> docker_git_insecure

Configures and instantiates a docker GIT without TLS or authentication.

```python
import pytest
import subprocess
from pathlib import Path
from pytest_docker_git_fixtures import DockerGITInsecure  # Optional, for typing

@pytest.mark.create_repo("test_docker_git_insecure")
def test_docker_git_insecure(docker_git_insecure: DockerGITInsecure, tmp_path: Path):
    uri = f"https://{docker_git_insecure.endpoint}/insecure/test_docker_git_insecure.git"
    path = tmp_path.join("local-clone")
    subprocess.run(
        ["git", "clone", uri, str(path)],
        check=True,
        cwd=str(tmp_path),
        stderr=subprocess.STDOUT,
    )
    assert path.exists()
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **created_repos** - The list of created repositories.
* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the insecure docker GIT service.
* **mirrored_repos** - The list of mirrored repositories.
* **service_name** - Name of the service within the docker-compose configuration.

Typing is provided by `pytest_docker_git_fixtures.DockerGITInsecure`.

### <a name="docker_git_password"></a> docker_git_password

Provides a generated password to use for authentication to the secure docker GIT service.

### <a name="docker_git_secure"></a> docker_git_secure

Configures and instantiates a TLS enabled docker GIT with HTTP basic authorization.

```python
import pytest
import subprocess
from pathlib import Path
from pytest_docker_git_fixtures import DockerGITSecure  # Optional, for typing

@pytest.mark.mirror_repo("https://github.com/crashvb/shim-bind.git")
def test_docker_git_secure(docker_git_secure: DockerGITSecure, tmp_path: Path):
    uri = f"https://{docker_git_secure.endpoint}/secure/shim-bind.git"
    path = tmp_path.join("local-clone")
    subprocess.run(
        ["git", "clone", uri, str(path)],
        check=True,
        cwd=str(tmp_path),
        stderr=subprocess.STDOUT,
    )
    assert path.joinpath("README.md").exists()
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **auth_header** - from [docker_git_auth_header](#docker_git_auth_header).
* **cacerts** - from [docker_git_cacerts](#docker_git_cacerts).
* **certs** - from [docker_git_certs](#docker_git_certs).
* **created_repos** - The list of created repositories.
* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the secure docker GIT service.
* **htpasswd** - from [docker_git_htpasswd](#docker_git_htpasswd)
* **mirrored_repos** - The list of mirrored repositories.
* **password** - from [docker_git_password](#docker_git_password).
* **service_name** - Name of the service within the docker-compose configuration.
* **ssl_context** - from [docker_git_ssl_context](#docker_git_ssl_context).
* **username** - from [docker_git_username](#docker_git_username).

Typing is provided by `pytest_docker_git_fixtures.DockerGITSecure`.

### <a name="docker_git_ssl_context"></a> docker_git_ssl_context

Provides an SSL context containing the CA trust store from the  [docker_git_cacerts](#docker_git_cacerts) fixture.

### <a name="docker_git_username"></a> docker_git_username

Provides a generated username to use for authentication to the secure docker GIT service.

## <a name="markers"></a>Markers

### pytest.mark.create_repo

This marker specifies the GIT repository(ies) that should be initialized within the docker GIT service(s) prior to testing. It can ...

... decorate individual tests:

```python
import pytest
from pytest_docker_git_fixtures import DockerGITSecure  # Optional, for typing

@pytest.mark.create_repo("test_docker_git_secure")
def test_docker_git_secure(docker_git_secure: DockerGITSecure):
	...
```

... be specified in the `pytestmark` list at the module level:

```python
#!/usr/bin/env python

import pytest

pytestmark = [pytest.mark.create_repo("test_generic_repo")]

...
```

... or be provided via the corresponding `--create-repo` command-line argument:

```bash
python -m pytest --create-repo repo0 --create-repo repo1 --create-repo repo2,repo3 ...
```

This marker supports being specified multiple times, and removes duplicate repository names (see [Limitations](#limitations) below).

A helper function, `get_created_repos`, is included for test scenarios that  wish to inspect the maker directly:

```python
import pytest
from pytest_docker_git_fixtures import DockerGITSecure, get_created_repos

@pytest.mark.create_repo("test_docker_git_secure")
def test_docker_git_secure(docker_git_secure: DockerGITSecure, request):
    name = get_created_repos(request)[0]
```

### pytest.mark.mirror_repo

Similarly to create_repo, this marker specifies the GIT repository(ies) that should be replicated to the docker GIT service(s) prior to testing.

Likewise, there is a `get_mirrored_repos` helper function.

## <a name="enumerated_fixtures"></a>Enumerated Fixtures

It is possible to instantiate multiple GIT instances using the corresponding enumerated fixtures. All [fixtures](#fixtures) listed above have _*_list_ (e.g. `docker_git_secure` -> `docker_git_secure_list`) versions that will return enumerated lists of corresponding data type.

For example:

```python
import requests
from typing import List  # Optional, for typing
from pytest_docker_git_fixtures import DockerGITSecure  # Optional, for typing

def test_docker_git_secure_list(docker_git_secure_list: List[DockerGITSecure]):
    for docker_git_secure in docker_git_secure_list:
        # Default listener ...
        response = requests.get(
            f"https://{docker_git_secure.endpoint}/",
            headers=docker_git_secure.auth_header,
            verify=str(docker_git_secure.cacerts),
        )
        assert response.status_code == 200
        assert response.content == b"pytest-docker-git-fixtures-docker\n"
```

It is possible to use both singular and enumerated fixtures within the same test context; however, the same values will be returned for the singular fixture as the first enumerated list value (i.e. docker_git_secure == docker_git_secure_list[0]). To avoid complications with lower layers, mainly docker-compose, and to allow for this interchangeability, caching is used internally.

By default, the scale factor of the enumerated instances is set to one (n=1). This value can be changed by overriding the `pdrf_scale_factor` fixture, as follows:

```python
import pytest

@pytest.fixture(scope="session")
def pdrf_scale_factor() -> int:
    return 4
```

This fixture will be used to scale both the insecure and secure docker GIT SCMs.

## <a name="limitations"></a>Limitations

1. All the fixtures provided by this package are <tt>session</tt> scoped; and will only be executed once per test execution.
2. The `create_repo`, and `mirror_repo` markers are processed as part of the `docker_git_insecure` and `docker_git_secure` fixtures. As such:
  * _all_ markers will be aggregated during initialization of the session, and processed prior test execution.
  * Initialized and mirror repositories will be applied to both the insecure and secure docker GIT SCMs, if both are instantiated.
3. At most 10 insecure and 10 secure docker GIT SCMs are supported using the embedded docker compose.
4. It is not currently possible to specify into which enumerated SCM instances repositories should be applied. As such, and for backwards compatibility, they will only be applied into the first instance of each of the insecure and secure docker GIT SCMs.

## Development

[Source Control](https://github.com/crashvb/pytest-docker-git-fixtures)
