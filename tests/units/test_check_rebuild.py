"""Tests for functions working on checkrebuild
"""

import subprocess
import pytest

from checkAUR.check_rebuild import check_rebuild # type: ignore [import-untyped]


def mock_raise_process_error(*args, **kwargs):
    """mock function for subprocess.run to raise the proper exception
    """
    raise subprocess.CalledProcessError(0, "empty")


def test_check_rebuild_unavailable(monkeypatch):
    """test for situation, when check rebuild is not available
    """
    monkeypatch.setattr("checkAUR.check_rebuild.subprocess.run", mock_raise_process_error)
    assert check_rebuild() == ()


class MockRunOutput:
    """mock class to replace output of subprocess.run
    """
    def __init__(self, stdout):
        self.stdout = stdout


@pytest.mark.parametrize("output, result", [
    ("foreign\tsome-package-git\nforeign some-package-2", ("some-package-git",)),
    ("foreign\tsome-package-git\nforeign\tsome-package-2\n", ("some-package-git","some-package-2")),
    ("some-package-git\nsome-package-2", ()),
    ("foreign\tsome-package-git\nldd /opt/some-path/another/0.1/libmissing.so\nlib-missing2.so => not found", ("some-package-git",)),
    ("", ()),
], scope="function")
def test_check_rebuild_outputs(monkeypatch, output, result):
    """test for possible results of checkrebuild
    """
    output = MockRunOutput(output.encode())
    monkeypatch.setattr("checkAUR.check_rebuild.subprocess.run", lambda _, **kwargs: output)
    assert check_rebuild() == result
