# 1. Check if the current directory is a Python project
# 2. Find the tests folder
# 3. Run the tests

import os
import pytest
import logging

logger = logging.getLogger("examine")


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
    ret = pytest.main(["tests"])
    if ret == pytest.ExitCode.OK:
        return 0
    elif ret == pytest.ExitCode.TESTS_FAILED:
        logger.info("Test failed")
        return 1
    
    elif ret == pytest.ExitCode.INTERRUPTED:
        logger.warn("Test interrupted")
        return 1
    elif ret == pytest.ExitCode.INTERNAL_ERROR:
        logger.warn("Test internal error")
        return 1
    elif ret == pytest.ExitCode.USAGE_ERROR:
        logger.warn("pytest is misused.")
        return 1
    elif ret == pytest.ExitCode.NO_TESTS_COLLECTED:
        logger.info("No tests collected")
        return 1




