import os
from pathlib import Path

import tomllib


def setup_environment(path: Path) -> None:
    """Loads a given `toml` file end set all values environment variables.

    * does not support nested `toml` files
    * only supports values that implement `__str__`
    * headers and keys are converted to uppercase and separated by an underscore

    :param path: A `Path` pointing to a `toml` file.
    """
    with open(path, "rb") as file:
        config: dict[str, dict[str, int | float | str]] = tomllib.load(file)

    for header in config.keys():
        for key, value in config[header].items():
            name = f"{header.upper()}_{key.upper()}"
            os.environ[name] = str(value)
