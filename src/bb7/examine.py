# 1. Check if the current directory is a Python project
# 2. Find the tests folder
# 3. Run the tests

import os
from pathlib import Path

import pytest

from .utils import cd, find_project_root


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

    proot = find_project_root()
    with cd(proot):
        src_path = Path(proot) / "src"

        subfolders = [f.name for f in src_path.iterdir() if f.is_dir()]
        module_name = subfolders[0]

    return pytest.main(args=[f"--cov={module_name}"])
