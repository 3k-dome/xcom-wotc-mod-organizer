import os
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
import time

import requests

RE_TITLE = re.compile(r"<div class=\"workshopItemTitle\">(.*?)</div>")
RE_AUTHOR = re.compile(r"<div class=\"friendBlockContent\">\s*(.*?)<br>")


@dataclass
class Mod:
    id: str
    path: str
    name: str
    title: str = field(default="")
    author: str = field(default="")
    active: bool = field(default=False)
    notes: list[str] = field(default_factory=list)
    modified: float = field(default_factory=float)

    def update_modified(self) -> None:
        self.modified = Path(self.path).parent.stat().st_mtime

    def __post_init__(self) -> None:
        if not self.title or not self.author:
            response = requests.get(f"{os.environ.get('STEAM_WORKSHOP_URL')}/?id={self.id}")
            if response.status_code == 200:
                self.title = RE_TITLE.findall(response.text)[0]
                self.author = ", ".join(RE_AUTHOR.findall(response.text))

            # look somewhat when doing this iteratively human (⌐■_■)
            time.sleep(random.uniform(0.3, 0.7))

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Mod):
            return self.id == __o.id
        raise NotImplementedError
