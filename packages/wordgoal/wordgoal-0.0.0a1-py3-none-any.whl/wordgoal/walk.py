from os import path
from pathlib import Path

from progrow import Rows, Style

from wordgoal.configuration import Configuration
from wordgoal.count import words_in_file


def graph_path(root: Path, file: Path, rows: Rows) -> None:
    rows.append(path.relpath(file, root), current=words_in_file(file), maximum=600)


def consider_directory(root: Path, consider: Path, rows: Rows) -> None:
    configuration = Configuration(consider)

    for object in consider.iterdir():
        if object.is_dir():
            if object.name in configuration.ignore:
                continue
            consider_directory(root=root, consider=object, rows=rows)
        elif object.is_file():
            if object.name.endswith(".md"):
                graph_path(root, object, rows)


def print_directory(path: Path) -> None:
    rows = Rows()
    consider_directory(root=path, consider=path, rows=rows)
    print(rows.render(Style(show_fraction=True)))
