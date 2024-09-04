import contextlib
import os
import uuid
from pathlib import Path
from typing import Iterator


@contextlib.contextmanager
def cd(path: str | Path) -> Iterator:
    """Can use like this: with cd(path): ..."""
    _old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(_old_cwd)


def find_project_root(cwd: str = ".", max_depth: int = 10) -> str | None:
    """Recursively find a `pyproject.toml` at given path or current working directory.
    If none if found, go to the parent directory, at most `max_depth` levels will be
    looked for.
    """
    original_path = Path(cwd).absolute()
    path = original_path
    for _ in range(max_depth):
        if path.joinpath("pyproject.toml").exists():
            return path.as_posix()
        if path.parent == path:
            # Root path is reached
            break
        path = path.parent
    return None


def random_mp3_fname(prefix: str = "bb7") -> str:
    return f"{prefix}_{uuid.uuid4()}.mp3"
