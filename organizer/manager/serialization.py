import json
from dataclasses import asdict, is_dataclass
from typing import Any, cast

from organizer import Category, Mod


class DataclassJSONEncoder(json.JSONEncoder):
    """Extends `JSONEncoder` to support `dataclasses`.

    credits: https://stackoverflow.com/a/51286749
    """

    def default(self, o: object):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


def serialize(cache_path: str, categories: list[Category]) -> None:
    """Serializes a `list` of `Categories` to JSON.

    :param cache_path: Path of the output JSON file.
    :param categories: A `list` of `Categories` to serialize.
    """
    with open(cache_path, "w") as cache:
        json.dump(categories, cache, cls=DataclassJSONEncoder, indent=4)


def deserialize_category(category: dict[str, Any]) -> Category:
    """Recursively deserialize a `Category` in plain `dict` format.

    Starts by creating an empty category. Then tries to get pares the
    category name from the given dict. Afterwards all mods in this category
    are deserialized (those are simple and flat entries). And lastly all
    subcategories are deserialized by calling this method recursively.

    :param category: A `Category` in `dict` format (i.e. from JSON parsing).
    :return: The deserialized `Category`.
    """
    result = Category()
    result.name = cast(str, category.get("name")) or result.name

    if mods := cast(list[dict[str, Any]] | None, category.get("mods")):
        result.mods = [Mod(**mod) for mod in mods]

    if sub_categories := cast(list[dict[str, Any]] | None, category.get("categories")):
        result.categories = [deserialize_category(sub_category) for sub_category in sub_categories]

    return result


def deserialize(cache_path: str) -> list[Category]:
    """Deserializes `Categories` from a parsed JSON file.

    :param cache_path: Path of the JSON file to deserialize.
    :return: All deserialized `Categories`.
    """
    with open(cache_path, "r") as cached:
        cached_categories = json.load(cached)
    return [deserialize_category(category) for category in cached_categories]
