import os
from typing import cast

from organizer.types.mod import Mod

from .local import LocalModDatabase
from .scan import convert, gather_paths


class ModLoader:
    def __init__(self) -> None:
        self.local = LocalModDatabase()
        self.workshop = cast(str, os.environ.get("WOTC_WORKSHOP_PATH"))

    def gather_installed(self) -> list[Mod]:
        """Gets all `Mods` that are currently installed.

        Gathers meta data for any `Mods` that are not yet cached.
        Updates the `modified` field for all mods and caches all of them
        before they are returned.

        :return: All currently installed `Mods`.
        """
        installed_paths = [*gather_paths(self.workshop)]
        installed_ids = {path.parent.stem for path in installed_paths}
        cached_ids = self.local.keys()

        mods: list[Mod] = []
        mods.extend(self.local.get_mods(cached_ids & installed_ids))
        mods.extend([convert(path) for id, path in zip(installed_ids, installed_paths) if id not in cached_ids])
        _ = [mod.update_modified() for mod in mods]

        self.local.insert_mods(mods)
        return mods

    def gather_active(self) -> None:
        ...
