from rich.table import Table
from rich.console import Console
from collections import OrderedDict
from typing import List

import sys
from .clipboard import Clipboard
from .weather import Weather
from .code_generator import CodePDFGenerator
from .api import CLIInterface

console = Console()


class Previous(CLIInterface):
    def __init__(self):
        super().__init__()


class Quit(CLIInterface):
    def __init__(self):
        super().__init__()


class CLI:
    def __init__(self, *args):
        super().__init__()
        self.custom_commands = []
        for arg in args:
            self.custom_commands.append(arg)
        self.quit = Quit()
        self.previous = Previous()

    def get_cli_list(self):
        aList: List[CLIInterface] = []
        for command in self.custom_commands:
            aList.append(command)
        return aList

    def traverse_menu(self, command: str, menu_items_list):
        for menu_item in menu_items_list:
            if f'{command}_children' in menu_item:
                return menu_item.get(f'{command}_children')
        return []

    def get_menu_items(self, cli: CLIInterface, command_stack: List[str]):
        menu_result = []
        menu_items_list = cli.retrieve_menu()
        if not command_stack:
            for menu_item in menu_items_list:
                menu_result.append(menu_item.get('menu_info'))
        else:
            for command in command_stack:
                menu_items_list = self.traverse_menu(command, menu_items_list)
            for menu_item in menu_items_list:
                menu_result.append(menu_item.get('menu_info'))
        return menu_result

    def initialize_main_menu_if_required(self, cli_list: List[CLIInterface], command_stack: List[str]):
        reached_cmd_deadend = len(cli_list) == 1 and self.get_menu_items(cli_list[0], command_stack) == []
        if not cli_list or not command_stack or reached_cmd_deadend:
            cli_list = self.get_cli_list()
            command_stack = []
        return (cli_list, command_stack, OrderedDict())

    def construct_menu_and_print(self, cli_list: List[CLIInterface], command_stack: List[str], menu_items_dict):
        shortcut = 'a'
        for cli in cli_list:
            for cli_menu in self.get_menu_items(cli, command_stack):
                menu_items_dict[shortcut] = (cli_menu, cli)
                shortcut = chr(ord(shortcut) + 1)
        if command_stack:
            menu_items_dict['p'] = (('previous', 'Go back to previous menu'), self.previous)
        menu_items_dict['q'] = (('quit', 'Quit application'), self.quit)

        if command_stack:
            console.print(' --> '.join(command_stack))
        table = Table()
        table.add_column('Key', justify='right', style='cyan', no_wrap=True)
        table.add_column('Command', style='magenta')
        table.add_column('Description', style='magenta')

        for key, value in menu_items_dict.items():
            table.add_row(key, value[0][0], value[0][1])
        console.print(table)

    def get_input_and_execute_logic(self, menu_items_dict, cli_list: List[CLIInterface], command_stack: List[str]):
        command = console.input('Please enter a command: ')
        if command in menu_items_dict:
            menu_chosen = menu_items_dict[command][0][0]
            cli_chosen = menu_items_dict[command][1]
            command_stack.append(menu_chosen)
            if cli_chosen is self.quit:
                console.print('Quitting CLI, have a nice day! :smiley:')
                sys.exit()
            elif cli_chosen is self.previous:
                command_stack = command_stack[:-2]
            else:
                try:
                    method = menu_items_dict[command][0][2]
                    if method:
                        if '#' in method:
                            method_params = method.split('#')
                            getattr(cli_chosen, method_params[0])(method_params[1])
                        else:
                            getattr(cli_chosen, method)()
                except Exception:
                    console.print_exception(show_locals=False)
            if cli_chosen is not self.previous:
                cli_list = [cli_chosen]
        else:
            console.print(f'{command} not recognized as a valid command!')
        return cli_list, command_stack

    def start(self):
        cli_list: List[CLIInterface] = []
        command_stack: List[str] = []
        while True:
            cli_list, command_stack, menu_items_dict = self.initialize_main_menu_if_required(cli_list, command_stack)
            self.construct_menu_and_print(cli_list, command_stack, menu_items_dict)
            cli_list, command_stack = self.get_input_and_execute_logic(menu_items_dict, cli_list, command_stack)


if __name__ == '__main__':
    cli = CLI(Weather(), Clipboard(), CodePDFGenerator())
    cli.start()
