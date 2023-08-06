from functools import cached_property
from logging import getLogger
from os.path import relpath
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from progrow import Rows
from yaml import safe_load

from wordgoal.config import Defaults, Files, Style
from wordgoal.document_types import DocumentType, get_document_type
from wordgoal.documents import markdown_goal, words_in_markdown, words_in_text


class Directory:
    """
    Directory walker.

    Arguments:
        path: File or directory.
    """

    def __init__(self, path: Path, parent: Optional["Directory"] = None) -> None:
        if not path.exists():
            raise FileNotFoundError(path)
        self.directory = path if path.is_dir() else path.parent
        self.file = path if path.is_file() else None

        self.logger = getLogger("wordgoal")
        self.parent = parent
        self.rows: Rows = parent.rows if parent else Rows()

        self.logger.debug("Created %s for: %s", self.__class__.__name__, path)

    def analyse_file(self, file: Path) -> None:
        self.logger.debug("Analysing file: %s", file)
        document_type = get_document_type(file.suffix)

        if document_type == DocumentType.MARKDOWN:
            count = words_in_markdown(file)
            goal = markdown_goal(file) or self.files.goal(file.name)
        elif document_type == DocumentType.TEXT:
            count = words_in_text(file)
            goal = self.files.goal(file.name)
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

    @cached_property
    def defaults(self) -> Defaults:
        return Defaults(
            parent=self.parent.defaults if self.parent else None,
            values=self.config.get("defaults", None),
        )

    @cached_property
    def files(self) -> Files:
        return Files(
            defaults=self.defaults,
            values=self.config.get("files", None),
        )

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

    @cached_property
    def style(self) -> Style:
        """ Gets this directory's style configuration. """
        return Style(
            parent=self.parent.style if self.parent else None,
            values=self.config.get("style", None),
        )

    def walk(self) -> None:
        """ Walks this directory. """

        directories: List[Path] = []
        files: List[Path] = []

        if self.file:
            files.append(self.file)
        else:
            for path in self.directory.iterdir():
                if self.ignore(path.name):
                    self.logger.debug('Ignoring "%s"', path.name)
                elif path.is_dir():
                    directories.append(path)
                elif path.is_file():
                    files.append(path)

        for directory in sorted(directories):
            Directory(path=directory, parent=self).walk()

        for path in sorted(files):
            self.analyse_file(path)
