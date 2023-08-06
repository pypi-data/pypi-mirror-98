from logging import getLogger
from pathlib import Path
from typing import Optional

from boringmd import front_matter_from_file, text_from_file
from yaml import safe_load

from wordgoal.documents.text import words_in_string

logger = getLogger("wordgoal")


def markdown_goal(file: Path) -> Optional[int]:
    """ Gets the document's goal from its front matter. """
    if fm := front_matter_from_file(file):
        try:
            return int(safe_load(fm)["goal"]["words"])
        except KeyError:
            pass
    logger.debug('"%s" does not prescribe a goal in its front matter', file)
    return None


def words_in_markdown(file: Path) -> int:
    """
    Returns the number of words in a Markdown file.

    Arguments:
        file: File.

    Returns:
        Word count.
    """
    return words_in_string(text_from_file(file))
