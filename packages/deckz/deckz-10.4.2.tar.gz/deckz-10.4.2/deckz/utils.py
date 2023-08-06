from itertools import chain
from pathlib import Path
from typing import FrozenSet, Optional

from git import Repo
from git.exc import InvalidGitRepositoryError
from yaml import safe_load

from deckz.exceptions import DeckzException


def get_section_config_paths(path: Path = Path(".")) -> FrozenSet[Path]:
    git_dir = get_git_dir(path)
    v1_ymls = git_dir.glob("**/section.yml")
    all_ymls = git_dir.glob("**/*.yml")
    vx_ymls = []
    for yml in all_ymls:
        with yml.open(encoding="utf8") as fh:
            content = safe_load(fh)
            if not isinstance(content, dict):
                continue
            if {"title", "version", "flavors"}.issubset(content):
                vx_ymls.append(yml)
    return frozenset(chain(v1_ymls, vx_ymls))


def get_git_dir(path: Path) -> Optional[Path]:
    try:
        repository = Repo(str(path), search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        raise DeckzException(
            "Could not find the path of the current git working directory. "
            "Are you in one?"
        ) from e
    return Path(repository.git.rev_parse("--show-toplevel")).resolve()
