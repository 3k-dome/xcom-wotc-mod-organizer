import glob
import re
from pathlib import Path
from typing import Iterable

from organizer.types import Mod

MOD_NAME_RE = r'^[^;]*?"([^"]+)"'


def gather_active(ini_path: str) -> set[str]:
    """Returns a `set` of all active `Mod`-names.

    :param ini_path: The path to the games mod ini.
    :return: A `set` of all active `Mod`-names.
    """
    with open(ini_path) as ini:
        content = ini.read()

    return set(re.findall(MOD_NAME_RE, content, re.MULTILINE))


def gather_paths(path: str) -> Iterable[Path]:
    """Gets the a `Path` for all installed mods.

    This scans though the mod folder and looks
    specifically for `XComMod`-files using a glob pattern.

    :param path: A path pointing to the mod directory.
    :return: An `Iterable` of all found `Paths`.
    """
    pattern = f"{path}\\*\\*.XComMod"
    results = glob.glob(pattern)
    return map(Path, results)


def convert(path: Path) -> Mod:
    """Converts a `Path` pointing to a mod into a `Mod`.

    :param path: A `Path` to convert.
    :return: The generated `Mod`.
    """
    return Mod(id=path.parent.stem, path=str(path), name=path.stem)
