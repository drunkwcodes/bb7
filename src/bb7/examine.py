# 1. Check if the current directory is a Python project
# 2. Find the tests folder
# 3. Run the tests

import os

import pytest


def examine_folders():
    if not os.path.isfile("pyproject.toml"):
        # not in the top of the project folder
        return False
    if not os.path.isdir("tests"):
        # no tests folder
        return False
    if not os.path.isdir("src"):
        # no src folder
        return False
    return True


def run_tests():
    # current_dir = os.getcwd()
    # print(current_dir)

    # return pytest.main([current_dir])
    return pytest.main()
