"""Main for checkAUR
"""

import logging
from pathlib import Path

import pyperclip # type: ignore [import-untyped]

from checkAUR.check_user import check_if_root
from checkAUR.check_rebuild import check_rebuild, print_invalid_packages
from checkAUR.aur_path import load_env
from checkAUR.use_git import pull_entire_aur
from checkAUR.compare_packages import compare_packages


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


def run_main(ignore=False, fetch=False):
    """run main program sequence

    Args:
        ignore (bool, optional): if checkrebuild should be ignored. Defaults to False.
        fetch (bool, optional): if only git fetch should be used. Defaults to False.

    Raises:
        NotImplementedError: _description_
    """
    if ignore:
        logging.debug("Running checkrebuild")
        try:
            invalid_packages = check_rebuild()
        except UnicodeError:
            message = "Error during analysis of checkrebuild results! Closing..."
            print(message)
            logging.critical(message)
            return
        logging.debug("Search results:")
        logging.debug(invalid_packages)
        print_invalid_packages(invalid_packages)
    else:
        invalid_packages = ()
    try:
        aur_path = load_env()
    except EnvironmentError:
        return

    logging.debug("Starting pulling repos")
    if fetch:
        raise NotImplementedError("Use of fetch not implemented!")
    pulled_packages = pull_entire_aur(aur_path)
    count_pulled_packages = len(pulled_packages)
    logging.debug("%s repos pulled", count_pulled_packages)
    compare_packages(pulled_packages, invalid_packages)
    if len(pulled_packages) != 0 or len(invalid_packages) != 0:
        copy_aur_wd(aur_path)


def main():
    """Main function for checkAUR
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        filename="logs.log",
        filemode="a"
    )
    logging.debug("Check user type")
    if check_if_root():
        return
    run_main()


if __name__ == "__main__":
    main()
