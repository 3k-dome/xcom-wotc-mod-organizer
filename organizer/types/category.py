import uuid
from dataclasses import dataclass, field
from functools import partial

from .mod import Mod


def uuid_factory(prefix: str) -> str:
    return prefix + str(uuid.uuid4())


@dataclass
class Category:
    id: str = field(init=False, default_factory=partial(uuid_factory, "Category-"))
    name: str = field(default="Unsorted")
    mods: list[Mod] = field(default_factory=list)
    categories: list["Category"] = field(default_factory=list)
