# 1. write tests
# 2. write code


import os
import logging
import pytest

logger = logging.getLogger("write")


def write_test_file():
    """write tests for each module"""

    """write tests for each module in src/ to corresponding test files in tests/"""

    src_dir = "./src/"
    test_dir = "./tests/"

    # 遍歷 src 目錄中的所有 Python 檔案
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if (
                file.endswith(".py")
                and file != "__init__.py"
                and file != "test_template.py"
            ):
                module_name = file[:-3]  # 去掉 .py 後綴
                module_path = os.path.join(root, file)

                # 計算對應的測試文件名和路徑
                relative_path = os.path.relpath(root, src_dir)
                test_file_dir = os.path.join(test_dir, relative_path)
                os.makedirs(test_file_dir, exist_ok=True)
                test_file_name = f"test_{module_name}.py"
                test_file_path = os.path.join(test_file_dir, test_file_name)

                if os.path.exists(test_file_path):
                    logger.info(f"Test file already exists: {test_file_path}")
                    continue

                with open(test_file_path, "w") as f:
                    pass

                logger.info(f"Generated test file for {module_name}: {test_file_path}")





def get_docstring(func: str) -> str:
    # Use pytest collect test functions' docstring
    item = pytest.Item.from_parent(name=func, parent=pytest.Function(func))
    return item.obj.__doc__
    


def write_code(func_name: str):
    # 1. get the docstring
    get_docstring()
    # 2. write code based on the tests' docstring
    


if __name__ == "__main__":
    write_test_file()
