import contextlib
import os
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


def find_project_root(cwd: str = ".", default: str = ".") -> Path:
    """Recursively find a `pyproject.toml` at given path or current working directory.
    If none if found, go to the parent directory, at most `max_depth` levels will be
    looked for.

    If no `pyproject.toml` is found, return the given `default` path.
    """
    path = Path(cwd).absolute()
    if list(path.glob("pyproject.toml")):
        return path
    if path == path.parent:
        # return None
        return Path(default)
    return find_project_root(str(path.parent))
