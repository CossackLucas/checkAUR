"""Module for common data classes
"""

from typing import NamedTuple
from pathlib import Path


class EnvVariables(NamedTuple):
    """aggregator class for used environment variables
    """
    aur_path: Path
