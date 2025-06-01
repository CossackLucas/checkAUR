"""Module responsible for Git operations
"""

from typing import Optional
from pathlib import Path
import logging
import os

from git import Repo
import git.exc

def check_if_correct_repo(repo_path: Path) -> Optional[Repo]:
    """check if repo has parameters expected from AUR

    Args:
        repo_path (Path): absolute path to the repository

    Raises:
        OSError: if no repo in the directory
        ValueError: if no directory at the path

    Returns:
        Optiona[Repo]: Repo object if it's corrent, None if it's not
    """
    assert isinstance(repo_path, Path)
    logging.debug("Checking repo in %s", repo_path.as_posix())
    try:
        repo = Repo(repo_path.as_posix())
    except git.exc.InvalidGitRepositoryError as exc:
        raise OSError(f"No repo in {repo_path.as_posix()}") from exc
    except git.exc.NoSuchPathError as exc:
        raise ValueError("Given directory does not exist") from exc

    if repo.bare:
        message = "The repo is bare"
        print(message)
        logging.warning(message)
        return None

    if not repo.remotes.origin.exists():
        message = "The repo does not have the origin"
        print(message)
        logging.warning(message)
        return None

    return repo


def pull_repo(repo_path: Path) -> bool:
    """perform 'git pull' on one repository under the given path

    Args:
        repo_path (Path): path to the repo's folder

    Returns:
        bool: True if operation was successful, False if not
    """
    assert isinstance(repo_path, Path)
    repo = check_if_correct_repo(repo_path)
    if repo is None:
        return False
    result = repo.remotes.origin.fetch()
    if result[0].commit.hexsha == repo.head.commit.hexsha:
        return False
    try:
        repo.remotes.origin.pull()
    except git.exc.GitCommandError:
        return False
    return True


def pull_entire_aur(aur_path: Path) -> tuple[str,...]:
    """perform 'git pull' on user's entire AUR folder

    Args:
        aur_path (Path): path to user's AUR folder

    Returns:
        tuple[str,...]: tuple of pulled package's names
    """
    assert isinstance(aur_path, Path)
    folder_list: list[str] = os.listdir(aur_path)
    repo_list = []
    for element in folder_list:
        checked_path = aur_path / element
        if checked_path.is_dir():
            repo_list.append(checked_path)

    update_packages: list[str] = []
    for repo in repo_list:
        if pull_repo(repo):
            update_packages.append(repo.stem)

    return tuple(update_packages)
