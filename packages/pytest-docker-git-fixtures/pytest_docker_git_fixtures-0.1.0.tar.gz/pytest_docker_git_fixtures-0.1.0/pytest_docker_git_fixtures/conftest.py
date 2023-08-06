#!/usr/bin/env python

"""Configures execution of pytest."""


def pytest_addoption(parser):
    """pytest add option."""
    # TODO: Figure out why pytest tries to load this file twice ?!?
    try:
        parser.addoption(
            "--create-repo",
            action="append",
            default=[],
            help="list of bare GIT repositories to be initialized within the pytest docker git scm",
        )
        parser.addoption(
            "--mirror-repo",
            action="append",
            default=[],
            help="list of remote GIT repositories to be mirrored within the pytest docker git scm",
        )
    except ValueError as exception:
        if "already added" not in str(exception):
            raise exception


def pytest_collection_modifyitems(config: "_pytest.config.Config", items):
    """pytest collection modifier."""

    # pytest fixtures of scope=session don't appear to be able to find markers using request.node.get_closest_marker().
    # Copy from markers to options here, and counteract for duplicate invocations / assignments when used in fixtures.
    for item in items:
        names = item.get_closest_marker("create_repo")
        if names:
            option = getattr(config.option, "create_repo", [])
            option.extend(names.args)
            setattr(config.option, "create_repo", option)
        uris = item.get_closest_marker("mirror_repo")
        if uris:
            option = getattr(config.option, "mirror_repo", [])
            option.extend(uris.args)
            setattr(config.option, "mirror_repo", option)


def pytest_configure(config: "_pytest.config.Config"):
    """pytest configuration hook."""
    config.addinivalue_line(
        "markers",
        "create_repo: list of bare GIT repositories to be initialized within the pytest docker git scm",
    )
    config.addinivalue_line(
        "markers",
        "mirror_repo: list of remote GIT repositories to be mirrored within the pytest docker git scm",
    )
