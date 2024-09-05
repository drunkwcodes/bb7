import os
import uuid

from bb7.utils import cd, find_project_root, random_mp3_fname


def test_cd():
    original_dir = os.getcwd()
    test_dir = "/tmp"

    with cd(test_dir):
        assert os.getcwd() == test_dir

    assert os.getcwd() == original_dir


def test_find_project_root():
    # 獲取當前測試文件的目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 調用 find_project_root 函數
    project_root = find_project_root()

    # 驗證 project_root 是否存在
    assert os.path.exists(project_root)

    # 驗證 project_root 是否包含一些典型的項目文件或目錄
    assert os.path.exists(os.path.join(project_root, "pyproject.toml"))
    assert os.path.exists(os.path.join(project_root, "tests"))

    # 驗證 current_dir 是否在 project_root 之下
    assert current_dir.startswith(project_root)


def test_random_mp3_fname():
    # 測試默認前綴
    result = random_mp3_fname()
    assert result.startswith("bb7_")
    assert result.endswith(".mp3")
    assert len(result) >= 40  # "bb7_" + 32 字符的 UUID + ".mp3"

    # 測試自定義前綴
    custom_prefix = "test"
    result = random_mp3_fname(prefix=custom_prefix)
    assert result.startswith(f"{custom_prefix}_")
    assert result.endswith(".mp3")

    # 驗證 UUID 部分
    uuid_part = result[len(custom_prefix) + 1 : -4]
    try:
        uuid.UUID(uuid_part)
    except ValueError:
        assert False, "生成的文件名中 UUID 部分無效"
