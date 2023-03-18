import os
import shelve
from pathlib import Path
from typing import Iterable

from organizer.types import Mod


class LocalModDatabase:
    def __init__(self) -> None:
        self.file: str = "mod_db.shelve"
        self.path: str = f"{os.environ.get('CACHE_PATH')}/{self.file}"
        Path(self.path).parent.mkdir(exist_ok=True)

    def insert_mod(self, mod: Mod) -> None:
        with shelve.open(self.path) as db:
            db[mod.id] = mod

    def insert_mods(self, mods: Iterable[Mod]) -> None:
        with shelve.open(self.path) as db:
            for mod in mods:
                db[mod.id] = mod

    def get_mod(self, key: str) -> Mod:
        with shelve.open(self.path) as db:
            return db[key]

    def get_mods(self, keys: set[str]) -> list[Mod]:
        with shelve.open(self.path) as db:
            return [db[key] for key in keys]

    def keys(self) -> set[str]:
        with shelve.open(self.path) as db:
            return {*db.keys()}
