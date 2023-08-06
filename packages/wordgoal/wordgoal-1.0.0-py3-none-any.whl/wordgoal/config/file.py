from wordgoal.config.defaults import Defaults
from wordgoal.types import FileDictionary


class File:
    """
    Describes a file's configuration.

    Arguments:
        defaults: Default configuration.
        values:   Configuration values.
    """

    def __init__(self, defaults: Defaults, values: FileDictionary) -> None:
        self.defaults = defaults
        self.values = values

    @property
    def goal(self) -> int:
        """ Gets this file's goal. """
        return int(self.values.get("goal", self.defaults.goal))
