import os
from typing import cast

from organizer.types.mod import Mod

from .local import LocalModDatabase
from .scan import convert, gather_paths, gather_active
import subprocess


class ModLoader:
    def __init__(self) -> None:
        self.local = LocalModDatabase()
        self.workshop = cast(str, os.environ.get("WOTC_WORKSHOP_PATH"))
        self.game_dir = cast(str, os.environ.get("WOTC_GAME_PATH"))
        self.ini_path = "\\XComGame\\Config\\DefaultModOptions.ini"
        self.exe_path = "\\Binaries\\Win64\\XCom2.exe"

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

    def gather_active(self, mods: list[Mod]) -> None:
        """Sans the games ini for active mods and sets loaded mods active if found.

        :param mods: All found installed mods.
        """
        active = gather_active(self.game_dir + self.ini_path)
        for mod in mods:
            mod.active = True if mod.name in active else False

    def get_installed(self) -> list[Mod]:
        """Get all installed `Mods`.

        :return: A `list` of all installed `Mods`.
        """
        mods = self.gather_installed()
        self.gather_active(mods)
        return mods

    def activate_mods(self, installed: list[Mod]) -> None:
        """Sets all active and installed `Mods` as active in the games ini.

        :param installed: All installed mods.
        """
        with open(self.game_dir + self.ini_path, "w") as ini:
            lines = ["[Engine.XComModOptions]\n", "\n"]
            lines.extend([f'ActiveMods="{mod.name}"\n' for mod in installed if mod.active])
            ini.writelines(lines)

    def launch(self) -> None:
        """Launches the game."""
        subprocess.call(
            [
                self.game_dir + self.exe_path,
                "-review",
                "-noRedScreens",
                "-noStartUpMovies",
                "-allowConsole",
            ]
        )
