import pytest

from bb7.examine import examine_folders
from bb7.utils import cd


def test_examine_folders():

    with cd("/home/drunkwcodes/projects/bb7"):
        assert examine_folders()

    with cd("/home/drunkwcodes/projects/bb7/src"):
        with pytest.raises(AssertionError):
            assert examine_folders()


def test_run_tests():
    pass
