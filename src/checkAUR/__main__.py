"""Main for checkAUR
"""

import logging
import os

from checkAUR.check_user import check_if_root
from checkAUR.check_rebuild import check_rebuild, print_invalid_packages
from checkAUR.aur_path import load_dotenv
from checkAUR.use_git import pull_entire_aur
from checkAUR.compare_packages import compare_packages


def run_main(ignore=False, fetch=False):
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
        aur_path = load_dotenv()
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
        os.chdir(aur_path)


def main():
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
