"""test module for usage of git inside the program
"""

from pathlib import Path
from collections import namedtuple

import pytest
import git.exc

from checkAUR.use_git import check_if_correct_repo, pull_repo, pull_entire_aur # type: ignore [import-untyped]


ROOT_PATH = Path("/")


@pytest.mark.parametrize("input_exception, output_exception", [
    (git.exc.InvalidGitRepositoryError, OSError),
    (git.exc.NoSuchPathError, ValueError)
], scope="function")
def test_check_repo_exceptions(monkeypatch, input_exception, output_exception):
    """test for all possible exceptions raised by git during the check
    """

    def raise_input_exceptions(*_):
        raise input_exception

    monkeypatch.setattr("checkAUR.use_git.Repo.__init__", raise_input_exceptions)
    with pytest.raises(output_exception):
        check_if_correct_repo(ROOT_PATH)


Commit = namedtuple("Commit", "hexsha")


class MockCommit:
    """Mock commit class
    """
    def __init__(self, import_hexsha):
        self.commit = Commit(hexsha=import_hexsha)


class MockOrigin:
    """Mock class for origin remote
    """
    def __init__(self, exists, commit="2137"):
        self._exists = exists
        self._commit = commit
        self.exception = None

    def exists(self):
        return self._exists

    def fetch(self):
        return [MockCommit(self._commit)]

    @property
    def set_exception(self):
        return self.exception
    
    @set_exception.setter
    def set_exception(self, exception):
        self.exception = exception

    def pull(self):
        if self.exception is not None:
            raise self.exception("Test use git")


Remotes = namedtuple("Remotes", "origin")


class MockRepo:
    """Mock replacement for Repo class
    """
    def __init__(self, bare=False, origin_exists=True, commit="2137"):
        self.bare = bare
        self.origin_exists = origin_exists
        self.remotes = Remotes(origin=MockOrigin(origin_exists))

        self.commit = commit

    def __eq__(self, other_repo):
        return bool(self.bare == other_repo.bare and self.origin_exists == other_repo.origin_exists)

    @property
    def head(self):
        return MockCommit(self.commit)


@pytest.mark.parametrize("bare,origin, result", [
    (False, True, True),    # bare: if repo is bare repository, origin: if origin exists, result: if repo is returned or None
    (False, False, False),
    (True, True, False),
    (True, False, False)
    ], scope="function")
def test_repo_types(monkeypatch, bare, origin, result):
    """test checking responses for different repo types
    """
    def mock_repo_init(*_):
        return MockRepo(bare, origin)

    monkeypatch.setattr("checkAUR.use_git.Repo", mock_repo_init)
    if result:
        assert check_if_correct_repo(ROOT_PATH) == MockRepo(bare, origin)
    else:
        assert check_if_correct_repo(ROOT_PATH) is None


@pytest.mark.parametrize("check_result, sha_equality, result", [
    (True, False, True),
    (True, True, False),
    (False, False, False),
    (False, True, False)
], scope="function")
def test_pull_single_repo(monkeypatch, check_result, sha_equality, result):
    """test for pulling single repo
    """
    if not check_result:
        repo = None
    else:
        if sha_equality:
            repo = MockRepo()
        else:
            repo = MockRepo(commit="1000")
    monkeypatch.setattr("checkAUR.use_git.check_if_correct_repo", lambda *_: repo)
    assert pull_repo(ROOT_PATH) is result


def test_pull_single_repo_exception(monkeypatch):
    """test checking reaction for git pull problems
    """
    repo = MockRepo(commit="1000")
    repo.remotes.origin.set_exception = git.exc.GitCommandError
    monkeypatch.setattr("checkAUR.use_git.check_if_correct_repo", lambda *_: repo)
    assert pull_repo(ROOT_PATH) is False


@pytest.mark.parametrize("packages, check, result", [
    (("package_1", "package_2", "package_3"), (True, True, True), ("package_1", "package_2", "package_3")),
    (("package_1", "package_2", "package_3"), (False, True, False), ("package_2",)),
    (("package_1", "package_2", "package_3"), (False, False, False), ()),
    (("package_1", "package_2", "package_3"), (True, False, False), ("package_1",))
], scope="function")
def test_pull_entire_aur(monkeypatch, tmp_path, packages, check, result):
    """test for pulling the entire AUR catalog
    """
    input_path = tmp_path
    for package in reversed(packages):
        new_folder = tmp_path / package
        new_folder.mkdir()

    def replace_pull_repo(path):
        return check[int(path.stem[-1])-1]

    monkeypatch.setattr("checkAUR.use_git.pull_repo", replace_pull_repo)
    assert pull_entire_aur(input_path) == result
