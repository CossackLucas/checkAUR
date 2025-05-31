#! /usr/bin/env python
"""Executable scripts
"""

import logging
import argparse
from pathlib import Path

from checkAUR.aur_path import set_aur_path
from checkAUR.check_user import check_if_root
from checkAUR.__main__ import run_main


def main_cli():
    """Main CLI launcher
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

    logging.debug("Setting parser")

    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("-s", "--set", type=Path, nargs=1, help="set AUR repos localization", metavar="/dir/path")
    parser.add_argument("-f", "--fetch", action="store_true", help="run fetch instead of pull")
    parser.add_argument("-i", "--ignore", action="store_false", help="ignore checkrebuild command")

    args = parser.parse_args()
    if args.set:
        logging.debug("Setting AUR localization")
        if not set_aur_path(Path(args.set[0])):
            logging.error("Setting was unsuccessful!")
        else:
            logging.debug("Setting AUR successful.")

    run_main(ignore=args.ignore, fetch=args.fetch)


if __name__ == "__main__":
    main_cli()
