from logging import getLogger
from pathlib import Path

logger = getLogger("wordgoal")


def words_in_string(text: str) -> int:
    """
    Counts the words in a string.

    Arguments:
        text: Body.

    Returns:
        Word count.
    """

    if not text:
        return 0

    count = 0
    lines = text.splitlines()

    if len(lines) == 1:
        for word in lines[0].split(" "):
            count += 1 if word else 0
        logger.debug('Line "%s" has %s word(s).', lines[0], count)
    else:
        for line in lines:
            count += words_in_string(line)
        logger.debug('String "%s" has %s word(s).', text, count)

    return count


def words_in_text(file: Path) -> int:
    """
    Counts the words in a plain text file.

    Arguments:
        file: File.

    Returns:
        Word count.
    """

    with open(file, "r") as stream:
        return words_in_string(stream.read())
