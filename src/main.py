from typing import Iterable, Sequence, TypeVar
_T = TypeVar("_T")

from file_handler import FileHandler
from argparse import ArgumentParser, Action
from getpass import getpass

class PasswordPromptAction(Action):
    def __init__(
            self, 
            option_strings: Sequence[str], 
            dest: str, 
            nargs: int | str | None = 0, # Take no argument after -p flag
            const: _T | None = None, 
            default: _T | str | None = None, 
            choices: Iterable[_T] | None = None, 
            required: bool = False, help: str | None = None, 
            metavar: str | tuple[str, ...] | None = None
        ) -> None:
        super().__init__(
            option_strings, 
            dest, 
            nargs, 
            const, 
            default, 
            type, 
            choices, 
            required, 
            help, 
            metavar
        )

    def __call__(self, parser, args, values, option_string=None):
        password = getpass()
        setattr(args, self.dest, password)

if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser(
        prog="file_encrypter",
        description="Encrypts files with password"
    )

    parser.add_argument("-d", "--decrypt", action="store_true", default=False)
    parser.add_argument("-p", "--password", dest="password", required=True, action=PasswordPromptAction)
    parser.add_argument("--env-path", dest="env_path", help="The path to the .env file to which the salt will be saved.")
    parser.add_argument("paths", nargs="+")

    args = parser.parse_args()

    decrypt = args.decrypt
    password = args.password
    env_path = args.env_path
    paths = args.paths

    # Initialize file handler
    file_handler = FileHandler(*paths, password=password, decrypt_flag=decrypt, env_path=env_path)
    file_handler.main()