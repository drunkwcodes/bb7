# 1. write tests
# 2. write code

import ast
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("write")
# logger.setLevel(logging.INFO)


def write_test_file():
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


def get_functions_and_classes(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    tree = ast.parse(file_content)

    functions = [
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    ]
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    return functions, classes


def write_tests(test_file_path, module_name: str | None = None):
    # TODO: battle test this
    module_name = module_name or Path(test_file_path).relative_to("./tests")
    # print(module_name)
    # print(module_name.parents[0])
    module_path = f"./src/{module_name.parents[0]}/{module_name.stem[5:]}.py"

    functions, classes = get_functions_and_classes(module_path)

    # 1. check if the module has tests
    test_functions = list(map(lambda func_name: f"test_{func_name}", functions))
    test_classes = list(map(lambda class_name: f"Test{class_name}", classes))

    # 2. write the test if not exists
    test_original_functions, test_origninal_classes = get_functions_and_classes(
        test_file_path
    )

    with open(test_file_path, "a", encoding="utf-8") as file:
        for f in test_functions:
            if f not in test_original_functions:
                file.write(f"def {f}():\n    pass\n\n")
            else:
                logger.info(f"Test function already exists: {f}")

        for c in test_classes:
            if c not in test_origninal_classes:
                file.write(f"class {c}:\n    pass\n\n")
            else:
                logger.info(f"Test class already exists: {c}")


def write_all_tests():
    for root, dirs, files in os.walk("./tests"):
        for file in files:
            if file.endswith(".py") and file != "test_template.py":
                test_file_path = os.path.join(root, file)
                write_tests(test_file_path)


def write_code():
    pass


if __name__ == "__main__":
    write_test_file()
