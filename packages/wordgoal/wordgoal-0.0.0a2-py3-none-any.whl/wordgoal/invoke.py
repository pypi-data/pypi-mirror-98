from argparse import ArgumentParser
from logging import basicConfig, getLogger, root
from pathlib import Path
from typing import List, Optional

from progrow import Style

from wordgoal.directory import Directory
from wordgoal.version import get_version


def invoke(args: Optional[List[str]] = None) -> int:
    basicConfig()

    try:
        print(invoke_unsafe(args))
        return 0
    except Exception as ex:
        getLogger("wordgoal").exception(ex)
        return 1


def invoke_unsafe(args: Optional[List[str]] = None) -> str:
    arg_parser = ArgumentParser(
        "wordgoal",
        description="wordgoal charts word count toward a goal.",
        epilog="Made with ❤️ by Cariad Eccleston: https://cariad.io",
    )

    arg_parser.add_argument(
        "--path",
        default=".",
        help="file or directory to scan",
        metavar="PATH",
    )

    arg_parser.add_argument(
        "--log-level",
        default="INFO",
        help="log level",
        metavar="LEVEL",
    )

    arg_parser.add_argument(
        "--version",
        action="store_true",
        help="print the version",
    )

    arg_parser.add_argument(
        "--width",
        help="width to draw",
    )

    parsed_args = arg_parser.parse_args(args)
    root.setLevel(parsed_args.log_level.upper())

    if parsed_args.version:
        return get_version()

    directory = Directory(Path(parsed_args.path))
    directory.walk()

    style = Style(
        show_fraction=True,
        width=int(parsed_args.width) if parsed_args.width else None,
    )

    return directory.rows.render(style)
