"""tests for comparing packages
"""

import pytest

from checkAUR.compare_packages import compare_invalid_packages # type: ignore [import-untyped]


@pytest.mark.parametrize("invalid_packages, pulled_packages, result", [
    (("package_1",),("package_2", "package_1", "package_3"),()),
    (("package_1",),("package_2", "package_3"),("package_1",)),
    ((),("package_1", "package_2", "package_3"),()),
    (("package_1","package_2"),("package_2", "package_3"),("package_1",)),
    (("package_1","package_2"),("package_3"),("package_1","package_2")),
    (("package_1",),(),("package_1",)),
    ((),(),())
    ], scope="function")
def test_compare_invalid_packages(invalid_packages, pulled_packages, result):
    """test of comparing invalid packages with pulled ones
    """
    assert compare_invalid_packages(pulled_packages, invalid_packages) == result
