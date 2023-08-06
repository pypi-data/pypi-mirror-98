from pathlib import Path
from typing import Any, Dict, List

from yaml import safe_load


class Configuration:
    def __init__(self, path: Path) -> None:
        self.values: Dict[str, Any] = {}
        try:
            with open(path.joinpath("wordgoal.yml"), "r") as stream:
                self.values = safe_load(stream)
        except FileNotFoundError:
            pass

    @property
    def ignore(self) -> List[str]:
        return self.values.get("ignore", [])
