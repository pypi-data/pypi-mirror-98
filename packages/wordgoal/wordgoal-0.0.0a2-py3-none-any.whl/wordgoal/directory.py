from functools import cached_property
from logging import getLogger
from os.path import relpath
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from progrow import Rows
from yaml import safe_load

from wordgoal.count import words_in_markdown_file, words_in_text_file
from wordgoal.document_types import DocumentType, get_document_type


class Directory:
    """
    Directory walker.

    Arguments:
        root: File or directory.
    """

    def __init__(self, directory: Path, parent: Optional["Directory"] = None) -> None:
        self.directory = directory
        self.logger = getLogger("wordgoal")
        self.parent = parent
        self.rows: Rows = parent.rows if parent else Rows()

        self.logger.debug("Created %s for: %s", self.__class__.__name__, directory)

    def analyse_file(self, file: Path) -> None:
        self.logger.debug("Analysing file: %s", file)
        document_type = get_document_type(file.suffix)

        if document_type == DocumentType.MARKDOWN:
            count = words_in_markdown_file(file)
            goal = 600
        elif document_type == DocumentType.TEXT:
            count = words_in_text_file(file)
            goal = 600
        else:
            return

        self.rows.append(
            name=file.name if file == self.root else relpath(file, self.root),
            current=count,
            maximum=goal,
        )

    @cached_property
    def config(self) -> Dict[str, Any]:
        """ Gets this directory's configuration. """
        try:
            with open(self.directory.joinpath("wordgoal.yml"), "r") as stream:
                return cast(Dict[str, Any], safe_load(stream))
        except FileNotFoundError:
            return {}

    def ignore(self, name: str) -> bool:
        """
        Indicates whether or not to ignore an object in this directory.

        Arguments:
            name: Filesystem object name.

        Returns:
            `True` to ignore the object.
        """
        return name in self.config.get("ignore", [])

    @property
    def root(self) -> Path:
        """ Gets the root directory of this walk. """
        return self.parent.root if self.parent else self.directory

    def walk(self) -> None:
        """ Walks this directory. """

        files: List[Path] = []

        for path in self.directory.iterdir():
            if self.ignore(path.name):
                self.logger.debug('Ignoring "%s"', path.name)
            elif path.is_dir():
                Directory(directory=path, parent=self).walk()
            elif path.is_file():
                files.append(path)

        for path in files:
            self.analyse_file(path)
