import glob
from pathlib import Path
from typing import Iterable

from organizer.types import Mod


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
