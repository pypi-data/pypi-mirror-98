from functools import cached_property
from typing import Optional

from wordgoal.types import StyleDictionary


class Style:
    """
    Describes a directory's style configuration.

    Arguments:
        parent: Parent directory's style configuration, if any.
        values: This directory's style configuration, if any.
    """

    def __init__(
        self,
        parent: Optional["Style"],
        values: Optional[StyleDictionary],
    ) -> None:
        self.parent = parent
        self.values = values

    @cached_property
    def color(self) -> bool:
        """ Gets whether or not to render in color. """
        if self.values and "color" in self.values:
            return bool(self.values["color"])
        elif self.parent:
            return self.parent.color
        else:
            return True

    @cached_property
    def fractions(self) -> bool:
        """ Gets whether or not to render fractions. """
        if self.values and "fractions" in self.values:
            return bool(self.values["fractions"])
        elif self.parent:
            return self.parent.fractions
        else:
            return True

    @cached_property
    def percentages(self) -> bool:
        """ Gets whether or not to render percentages. """
        if self.values and "percentages" in self.values:
            return bool(self.values["percentages"])
        elif self.parent:
            return self.parent.percentages
        else:
            return False
