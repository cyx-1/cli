from rich.console import Console
from .api import CLIInterface
import pyperclip
import pathlib


class Clipboard(CLIInterface):
    def __init__(self):
        super().__init__()
        self.console = Console()

    def print_command(self):
        self.console.print(f'{pyperclip.paste()}')

    def uppercase_command(self):
        content = pyperclip.paste()
        content = content.upper()
        pyperclip.copy(content)
        self.console.print(f'{content}')

    def file_uri_command(self):
        content = pyperclip.paste()
        content = pathlib.Path(content).as_uri()
        pyperclip.copy(content)
        self.console.print(f'{content}')

    def retrieve_menu(self):
        return [
            {
                "menu_info": ["clipboard", "Perform actions on clipboard content", ""],
                "clipboard_children": [
                    {"menu_info": ['print', 'Print out content of clipboard onto console', 'print_command']},
                    {"menu_info": ['uppercase', 'turn clipboard content to uppercase', 'uppercase_command']},
                    {"menu_info": ['file_uri', 'convert clipboard content to file uri format', 'file_uri_command']},
                ],
            }
        ]
