import os
from itertools import chain
from pathlib import Path

from ..types import Category, Mod
from .serialization import deserialize, serialize


class Manager:
    def __init__(self) -> None:
        self.file: str = "settings.json"
        self.path: str = f"{os.environ.get('CACHE_PATH')}/{self.file}"
        Path(self.path).parent.mkdir(exist_ok=True)

        self.categories = []
        if Path(self.path).is_file():
            self.categories = deserialize(self.path)

    def update(self, installed: set[Mod]) -> None:
        managed = set(self.flatten())
        unmanaged = installed - managed
        self.insert(unmanaged)
        uninstalled = managed - installed
        self.remove(uninstalled)

    def serialize(self) -> None:
        serialize(self.path, self.categories)

    def __flatten(self, category: Category) -> list[Mod]:
        mods = category.mods
        if category.categories:
            _ = [mods.extend(self.__flatten(sub_category)) for sub_category in category.categories]
        return mods

    def flatten(self) -> list[Mod]:
        mods = [self.__flatten(category) for category in self.categories]
        return [*chain(*mods)]

    def __remove(self, category: Category, mods: set[Mod]) -> None:
        category.mods = [mod for mod in category.mods if mod not in mods]
        _ = [self.__remove(sub_category, mods) for sub_category in category.categories]

    def remove(self, mods: set[Mod]) -> None:
        _ = [self.__remove(category, mods) for category in self.categories]

    def __insert(self, id: str = "") -> int:
        if id:
            return next((i for i, category in enumerate(self.categories) if category.id == id), -1)
        return next((i for i, category in enumerate(self.categories) if category.name == "Unsorted"), -1)

    def insert(self, mods: set[Mod]) -> None:
        unsorted_index = self.__insert()
        if unsorted_index != -1:
            self.categories[unsorted_index].mods.extend(mods)
            return

        category = Category()
        category.mods.extend(mods)
        self.categories.insert(0, category)

    def insert_at(self, id: str, index: int, mod: Mod) -> None:
        unsorted_index = self.__insert(id)
        if unsorted_index != -1:
            self.categories[unsorted_index].mods.insert(index, mod)

    def find(self, id: str) -> Mod:
        return next((mod for mod in self.flatten() if mod.id == id))

    def __flatten_category(self, category: Category) -> list[Category]:
        results = [category]
        if category.categories:
            _ = [results.extend(self.__flatten_category(sub_category)) for sub_category in category.categories]
        return results

    def flatten_categories(self) -> list[Category]:
        return [*chain(*[self.__flatten_category(category) for category in self.categories])]

    def find_category(self, id: str) -> Category:
        return next((category for category in self.flatten_categories() if category.id == id))

    def __remove_category(self, category: Category, remove: Category) -> None:
        category.categories = [x for x in category.categories if x.id != remove.id]
        _ = [self.__remove_category(sub_category, remove) for sub_category in category.categories]

    def remove_category(self, remove: Category) -> None:
        _ = [self.__remove_category(category, remove) for category in self.categories]

    def new_category(self, name: str) -> None:
        self.categories.append(Category(name))
