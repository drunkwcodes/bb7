# 1. Check if the current directory is a Python project
# 2. Find the tests folder
# 3. Run the tests

import os


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
    pass
