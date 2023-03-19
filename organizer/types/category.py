from dataclasses import dataclass, field

from .mod import Mod


@dataclass
class Category:
    name: str = field(default="Unsorted")
    mods: list[Mod] = field(default_factory=list)
    categories: list["Category"] = field(default_factory=list)