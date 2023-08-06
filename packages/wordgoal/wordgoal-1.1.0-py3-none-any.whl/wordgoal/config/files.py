from typing import Dict, Optional

from wordgoal.config.defaults import Defaults
from wordgoal.config.file import File
from wordgoal.types import FileDictionary


class Files:
    """
    Describes the configurations of a collection of files.

    Arguments:
        defaults: Default configuration.
        values:   Configuration values.
    """

    def __init__(
        self,
        defaults: Defaults,
        values: Optional[Dict[str, FileDictionary]] = None,
    ) -> None:
        self.defaults = defaults
        self.values: Dict[str, FileDictionary] = values or {}

    def file(self, filename: str) -> Optional[File]:
        """
        Gets a file's configuration.

        Argument:
            filename: Filename.

        Returns:
            Configuration, if any.
        """
        if values := self.values.get(filename):
            return File(values=values, defaults=self.defaults)
        return None

    def goal(self, filename: str) -> int:
        """
        Gets a file's goal.

        Argument:
            filename: Filename.

        Returns:
            Goal.
        """
        if file := self.file(filename):
            return file.goal
        return self.defaults.goal
