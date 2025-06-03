"""Module responsible for Git operations
"""

from typing import Optional
from pathlib import Path
import os

from git import Repo
import git.exc

from checkAUR.common.custom_logging import logger
from checkAUR.common.exceptions import ProgramNotInstalledError


def check_pkg_build(repo_path: Path) -> bool:
    """check if under given directory there is an PKGBUILD file

    Args:
        repo_path (Path): path to potential repo

    Returns:
        bool: True if there is PKGBUILD file under given path
    """
    pkgbuild_file = repo_path / "PKGBUILD"
    return bool(pkgbuild_file.exists() and pkgbuild_file.is_file())


def check_if_correct_repo(repo_path: Path) -> Optional[Repo]:
    """check if repo has parameters expected from AUR

    Args:
        repo_path (Path): absolute path to the repository

    Raises:
        OSError: if no repo in the directory
        ValueError: if no directory at the path
        ProgramNotInstalledError: if Git is not installed

    Returns:
        Optional[Repo]: Repo object if it's correct, None if it's not
    """
    assert isinstance(repo_path, Path)
    logger.debug("Checking repo in %s", repo_path.as_posix())
    try:
        repo = Repo(repo_path.as_posix())
    except git.exc.InvalidGitRepositoryError as exc:
        message = f"No repo in {repo_path.as_posix()}"
        logging.error(message)
        raise OSError(message) from exc
    except git.exc.NoSuchPathError as exc:
        message = f"Given directory {repo_path.as_posix()} does not exist"
        logging.error(message)
        raise ValueError(message) from exc
    except git.exc.GitCommandNotFound as exc:
        message = "Git not installed!"
        print(message)
        logger.critical(message)
        raise ProgramNotInstalledError("Git") from exc

    if repo.bare:
        message = "The repo is bare"
        print(message)
        logger.warning(message)
        return None

    if not repo.remotes.origin.exists():
        message = "The repo does not have the origin"
        print(message)
        logger.warning(message)
        return None

    if not check_pkg_build(repo_path):
        message = "The repo does not have PKGBUILD file"
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
    
    Raises:
        ProgramNotInstalledError: if Git is not installed
    """
    assert isinstance(repo_path, Path)
    try:
        repo = check_if_correct_repo(repo_path)
    except (OSError, ValueError):
        return False
    except ProgramNotInstalledError as exc:
        raise ProgramNotInstalledError(exc.program) from exc

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
    repo_list: tuple[Path,...] = tuple(checked_path for element in folder_list if (checked_path := aur_path/element).is_dir())

    try:
        return tuple(repo.stem for repo in repo_list if pull_repo(repo))
    except ProgramNotInstalledError as exc:
        raise ProgramNotInstalledError(exc.program) from exc
