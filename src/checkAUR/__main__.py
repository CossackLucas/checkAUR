"""Main for checkAUR
"""

from pathlib import Path

import pyperclip # type: ignore [import-untyped]

from checkAUR.common.custom_logging import logger
from checkAUR.check_user import check_if_root
from checkAUR.check_rebuild import check_rebuild, print_invalid_packages
from checkAUR.aur_path import load_env
from checkAUR.use_git import pull_entire_aur
from checkAUR.compare_packages import compare_packages
from checkAUR.common.exceptions import ProgramNotInstalledError


def copy_aur_wd(aur_path: Path) -> None:
    """copy 'cd /aur/path' command into clipboard. Current solution to cwd problem

    Args:
        aur_path (Path): path to user's AUR folders

    Raises:
        TypeError: if aur_path is of the wrong type
    """
    if not isinstance(aur_path, Path):
        raise TypeError("Path should be pathlib.Path type!") 
    pyperclip.copy(f"cd {aur_path.as_posix()}")
    print("Command to get to AUR folder was copied into the clipboard.")


def run_main(ignore=False) -> None:
    """run main program sequence

    Args:
        ignore (bool, optional): if checkrebuild should be ignored. Defaults to False.
    """
    if ignore:
        logger.debug("Running checkrebuild")
        try:
            print("Starting check-rebuild...")
            invalid_packages = check_rebuild()
        except UnicodeError:
            message = "Error during analysis of checkrebuild results! The step will be skipped"
            print(message)
            logger.error(message)
            invalid_packages = ()
        except ProgramNotInstalledError as exc:
            print(str(exc))
            print("Check if it's installed, install it using pacman or use -i flag. The step will be skipped")
            invalid_packages = ()
        logger.debug("Search results:")
        logger.debug(invalid_packages)
        print_invalid_packages(invalid_packages)
    else:
        invalid_packages = ()

    try:
        env_variables = load_env()
        aur_path = env_variables.aur_path
    except EnvironmentError:
        return

    logger.debug("Starting pulling repos")
    try:
        pulled_packages = pull_entire_aur(aur_path)
    except ProgramNotInstalledError:
        print("Closing...")
        return

    count_pulled_packages = len(pulled_packages)
    logger.debug("%s repos pulled", count_pulled_packages)
    compare_packages(pulled_packages, invalid_packages)

    if len(pulled_packages) != 0 or len(invalid_packages) != 0:
        copy_aur_wd(aur_path)


def main():
    """Main function for checkAUR
    """
    logger.debug("Main interface start")
    if check_if_root():
        return
    run_main()


if __name__ == "__main__":
    main()
