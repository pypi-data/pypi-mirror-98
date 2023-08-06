from logging import getLogger
from pathlib import Path

from boringmd import from_file


def words_in_line(line: str) -> int:
    count = 0
    for chunk in line.split(" "):
        if chunk:
            count += 1
    return count


def words_in_file(path: Path) -> int:
    logger = getLogger("wordgoal")
    plain = from_file(path)
    total = 0
    for line in plain.splitlines():
        if not line:
            continue
        count = words_in_line(line)
        logger.debug('Line "%s" has %s word%s.', line, count, "" if count == 1 else "s")
        total += count
    return total
