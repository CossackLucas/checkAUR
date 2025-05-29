#! /usr/bin/env python
"""Executable scripts
"""

import logging
import argparse
from pathlib import Path

from checkAUR.aur_path import set_aur_localization


def main_cli():
    """Main CLI launcher
    """
    logging.basicConfig(level=logging.CRITICAL, format="%(levelname)s:%(name)s:%(message)s")
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug("Setting parser")

    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("-s", "--set", type=Path, nargs=1, help="set AUR repos localization")
    parser.add_argument("-f", "--fetch", action="store_true", help="run fetch instead of pull")
    parser.add_argument("-i", "--ignore", action="store_true", help="ignore checkrebuild command")

    args = parser.parse_args()
    if args.set:
        logging.debug("Setting AUR localization")
        if not set_aur_localization(args.set):
            logging.warning("Setting was unsuccessful!")
            return
        logging.debug("Setting AUR successful.")

    if args.ignore:
        print("I ignore")

    if args.fetch:
        print("Just fetching")

    print("Nothing")
