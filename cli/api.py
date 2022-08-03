from typing import Dict, List


class CLIInterface:
    def retrieve_menu(self) -> List[Dict[str, List[str]]]:
        '''
        This method defines a command line interface menu by returning a list of dictionary, menu dictionary.\n
        Each dictionary has a key of 'menu_info' to represent an entry in the menu system. \n
        dictionary value of 'menu_info' contains the 1) menu name 2) menu description and 3) the method to invoke\n
        To depict a submenu, add a key to the dictionary with value of menu name along with suffix of '_children'\n
        and the value of that submenu key becomes a list of menu dictionary again\n
        Illustrative example:\n
        [
            {"menu_info": ['search topic', 'search and display result in vscode', 'fuzzy_search']},
            {
                "menu_info": ['goto topic', 'display favorite topics in vscode', ''],
                "goto topic_children": [
                    {"menu_info": ['2nd_brain', 'notes on 2nd brain implementation', 'jump_to#2ndbrain Notes']},
                ],
            }
        ]
        '''
        pass
