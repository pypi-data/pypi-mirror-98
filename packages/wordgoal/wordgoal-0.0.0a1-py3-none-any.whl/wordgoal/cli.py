from argparse import ArgumentParser
from logging import basicConfig, getLogger, root
from pathlib import Path
from typing import List, Optional

from colorama import Style

from wordgoal.walk import print_directory


class CLI:
    """
    CLI executor.

    Arguments:
        args: Arguments. Will read from the command line if omitted.
    """

    def __init__(self, args: Optional[List[str]] = None) -> None:
        basicConfig()
        self.logger = getLogger("wordgoal")

        wordgoal = str(Style.BRIGHT) + "wordgoal" + str(Style.RESET_ALL)

        description = f"{wordgoal} graphs your word count towards a goal."

        self.arg_parser = ArgumentParser(
            "wev",
            description=description,
        )

        self.arg_parser.add_argument(
            "--log-level",
            default="INFO",
            help="log level (default is INFO)",
            metavar="LEVEL",
        )

        self.arg_parser.add_argument(
            "--version",
            action="store_true",
            help="print the version",
        )

        self.args = self.arg_parser.parse_args(args)
        root.setLevel(self.args.log_level.upper())

    def invoke(self) -> int:
        """
        Invokes the appropriate task for the given command line arguments

        Returns:
            Shell return code.
        """
        print_directory(Path("."))
        return 0
        # try:
        #     return self.try_invoke()
        # except CannotResolveError as ex:
        #     self.logger.critical(ex)
        #     return 1
        # except Exception as ex:
        #     self.logger.exception(ex)
        #     return 2

    # def try_invoke(self) -> int:
    #     """
    #     Attempts to invokes the appropriate task for the given command line
    #     arguments. Could raise any exceptions.

    #     Returns:
    #         Shell return code.
    #     """
    #     if self.args.command:
    #         return execute(command=self.args.command)
    #     elif self.args.explain:
    #         explain()
    #     elif self.args.version:
    #         print(get_version())
    #     else:
    #         self.arg_parser.print_help()
    #     return 0
