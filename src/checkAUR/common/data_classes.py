"""Module for common data classes
"""

from typing import NamedTuple
from pathlib import Path

from checkAUR.common.package import Package


class EnvVariables(NamedTuple):
    """aggregator class for used environment variables
    """
    aur_path: Path


class TuplePackages(NamedTuple):
    """tuple type aggregating all used collections of packages
    """
    aur_packages: set[Package]
    pacman_packages: set[Package]
    pulled_packages: set[Package]
    invalid_packages: set[str]
