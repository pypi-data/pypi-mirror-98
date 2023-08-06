from functools import cached_property
from typing import Optional

from wordgoal.types import DefaultsDictionary


class Defaults:
    """
    Describes a directory's default configuration.

    Arguments:
        parent: Parent directory's configuration, if any.
        values: This directory's configuration, if any.
    """

    def __init__(
        self,
        parent: Optional["Defaults"],
        values: Optional[DefaultsDictionary],
    ) -> None:
        self.parent = parent
        self.values = values

    @cached_property
    def goal(self) -> int:
        """ Gets the default goal for files in this directory. """
        if self.values and "goal" in self.values:
            return int(self.values["goal"])
        elif self.parent:
            return self.parent.goal
        else:
            return 1000
