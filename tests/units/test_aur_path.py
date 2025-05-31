"""Tests for setting repos path
"""
from pathlib import Path
import os
import pytest

from checkAUR.aur_path import set_aur_path, setting_env_variable # type: ignore [import-untyped]


ROOT_PATH = Path("/")


def raise_io_exception(**kwargs):
    """raise mock IO exception
    """
    raise IOError()


def test_no_env(monkeypatch):
    """test no access to environment variables
    """
    monkeypatch.delenv("aur_path", raising=False)
    monkeypatch.setattr("checkAUR.aur_path.find_dotenv", raise_io_exception, raising=True)
    with pytest.raises(EnvironmentError):
        setting_env_variable(ROOT_PATH)


def test_only_dotenv(monkeypatch):
    """test only .env
    """
    def mock_aur_path(*_):
        monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())

    monkeypatch.delenv("aur_path", raising=False)
    monkeypatch.setattr("checkAUR.aur_path.set_key", mock_aur_path)

    setting_env_variable(aur_path=ROOT_PATH)
    assert os.environ.get("aur_path") is ROOT_PATH.as_posix()


def test_only_environ(monkeypatch):
    """test only system environment variable
    """
    monkeypatch.setattr("checkAUR.aur_path.find_dotenv", raise_io_exception, raising=True)
    monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())

    setting_env_variable(aur_path=ROOT_PATH)
    assert os.environ.get("aur_path") is ROOT_PATH.as_posix()


def test_both_env_var(monkeypatch):
    """test when both options are available
    """
    def mock_aur_path(*_):
        monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())

    monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())
    monkeypatch.setattr("checkAUR.aur_path.set_key", mock_aur_path)

    setting_env_variable(aur_path=ROOT_PATH)
    assert os.environ.get("aur_path") is ROOT_PATH.as_posix()


@pytest.fixture(scope="module", name="folder_on_drive")
def folder_on_drive_fixture(tmp_path_factory):
    """create temp folder for tests
    """
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="module", name="file_on_drive")
def file_on_drive_fixture(folder_on_drive):
    """create temp file in already created temp folder
    """
    result_path = folder_on_drive / ".file"
    with open(result_path, "w", encoding="utf-8"):
        pass
    return result_path


@pytest.fixture(scope="module")
def relative_folder_on_drive(folder_on_drive):
    """create relative path for test folder
    """
    return folder_on_drive.relative_to(folder_on_drive)


@pytest.fixture(scope="module")
def relative_file_on_drive(folder_on_drive, file_on_drive):
    """create relative path for test file
    """
    return file_on_drive.relative_to(folder_on_drive)


@pytest.mark.parametrize("input_path,result", [
    ("folder_on_drive", True),
    ("file_on_drive", False),
    ("relative_folder_on_drive",False),
    ("relative_file_on_drive", False),
    (Path("/sth/sth"), False),
    (Path("/stg/sth/path.file"), False),
    (Path("wrong/relative/path"), False),
    (Path("wrong/relative/path.file"), False),
    ("/str/as/path", False),
    (123, False),
    (123.123232, False)
    ])
def test_different_paths(monkeypatch, input_path, result, request):
    """test possible inpute paths
    """
    monkeypatch.setenv("aur_path", "/")
    if isinstance(input_path, str) and "on_drive" in input_path:
        input_path = request.getfixturevalue(input_path)
    assert set_aur_path(input_path) == result
