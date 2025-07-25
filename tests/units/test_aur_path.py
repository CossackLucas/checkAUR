"""Tests for setting repos path
"""
from pathlib import Path
import os
import pytest

from checkAUR.aur_path import set_aur_path,setting_path_env_variable # type: ignore [import-untyped]
from checkAUR.aur_path import load_env # type: ignore [import-untyped]
from checkAUR.common.data_classes import EnvVariables # type: ignore [import-untyped]


ROOT_PATH = Path("/")


def raise_io_exception(**kwargs):
    """raise mock IO exception
    """
    raise IOError()


def test_no_env(monkeypatch):
    """test no access to environment variables
    """
    monkeypatch.delenv("aur_path", raising=False)
    monkeypatch.setattr("checkAUR.aur_path.dotenv.find_dotenv", raise_io_exception, raising=True)
    assert os.environ.get("aur_path", ROOT_PATH.as_posix())


def test_only_dotenv(monkeypatch):
    """test only .env
    """
    def mock_aur_path(*_):
        monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())

    monkeypatch.delenv("aur_path", raising=False)
    monkeypatch.setattr("checkAUR.aur_path.dotenv.set_key", mock_aur_path)

    setting_path_env_variable(aur_path=ROOT_PATH)
    assert os.environ.get("aur_path") is ROOT_PATH.as_posix()


def test_only_environ(monkeypatch):
    """test only system environment variable
    """
    monkeypatch.setattr("checkAUR.aur_path.dotenv.find_dotenv", raise_io_exception, raising=True)
    monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())

    setting_path_env_variable(aur_path=ROOT_PATH)
    assert os.environ.get("aur_path") is ROOT_PATH.as_posix()


def test_both_env_var(monkeypatch):
    """test when both options are available
    """
    def mock_aur_path(*_):
        monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())

    monkeypatch.setenv("aur_path", ROOT_PATH.as_posix())
    monkeypatch.setattr("checkAUR.aur_path.dotenv.set_key", mock_aur_path)

    setting_path_env_variable(aur_path=ROOT_PATH)
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
    ("relative_folder_on_drive", False),
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

    monkeypatch.setattr("checkAUR.aur_path.setting_path_env_variable", lambda *_: None)
    assert set_aur_path(input_path) == result


@pytest.mark.parametrize("dotenv_status, variable_status", [
    (True, False),
    (False, False)
], scope="function")
def test_load_env_error(monkeypatch, dotenv_status, variable_status):
    """tests for errors in loading environment variables
    """
    def mock_find_dotenv(**_):
        if not dotenv_status:
            raise IOError

    monkeypatch.setattr("checkAUR.aur_path.dotenv.find_dotenv", mock_find_dotenv)
    monkeypatch.setattr("checkAUR.aur_path.dotenv.load_dotenv", lambda *_: "/")
    if variable_status:
        monkeypatch.setenv("aur_path", "value")
    else:
        monkeypatch.delenv("aur_path", raising=False)
    with pytest.raises(EnvironmentError):
        load_env()


@pytest.mark.parametrize("dotenv_status, env_status", [
    (True, True),
    (True, False),
    (False, True),
], scope="function")
def test_load_env(monkeypatch, dotenv_status, env_status):
    """tests for loading environment variables
    """
    def mock_find_dotenv(**_):
        if not dotenv_status:
            raise IOError

    def mock_load_dotenv(*_):
        if not env_status:
            monkeypatch.setenv("aur_path", "/")

    monkeypatch.setattr("checkAUR.aur_path.dotenv.find_dotenv", mock_find_dotenv)
    monkeypatch.setattr("checkAUR.aur_path.dotenv.load_dotenv", mock_load_dotenv)
    if env_status:
        monkeypatch.setenv("aur_path", "/")
    else:
        monkeypatch.delenv("aur_path")
    assert load_env() == EnvVariables(aur_path=Path("/"))
