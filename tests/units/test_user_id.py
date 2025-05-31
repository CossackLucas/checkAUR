"""Test for running as root
"""

import pytest
from checkAUR.check_user import check_if_root # type: ignore [import-untyped]

@pytest.mark.parametrize("user_id, result", [(0,True), (1000, False), (1050, False)], scope="function")
def test_user_id(monkeypatch, user_id, result):
    """test to check if user is root
    """
    monkeypatch.setattr("checkAUR.check_user.os.getuid", lambda: user_id)
    assert check_if_root() == result
