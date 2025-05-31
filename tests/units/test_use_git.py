"""test module for usage of git inside the program
"""
#Todo: only started. Finish those tests

from pathlib import Path

import pytest
import git.exc

from checkAUR.use_git import check_if_correct_repo # type: ignore [import-untyped]


@pytest.mark.parametrize("input_exception, output_exception", [
    (git.exc.InvalidGitRepositoryError, OSError),
    (git.exc.NoSuchPathError, ValueError)
], scope="function")
def test_check_repo_exceptions(monkeypatch, input_exception, output_exception):
    """test for all possible exceptions raised by git during the check
    """

    def raise_repo_exceptions(*_):
        raise input_exception

    monkeypatch.setattr("checkAUR.use_git.Repo.__init__", raise_repo_exceptions)
    with pytest.raises(output_exception):
        check_if_correct_repo(Path("/"))
