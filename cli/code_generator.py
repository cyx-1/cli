from rich.console import Console
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers.jvm import JavaLexer
from pygments.lexers.javascript import JavascriptLexer, TypeScriptLexer
from pygments.formatters import HtmlFormatter
from typing import List
from rich.prompt import Prompt
import pdfkit
import subprocess
import os
import sys
from .api import CLIInterface


class CodePDFGenerator(CLIInterface):
    def retrieve_menu(self):
        return [{"menu_info": ['code to pdf', 'generate PDF from source code with syntax highlighting', 'generate_pdf']}]

    def __init__(self):
        super().__init__()
        self.console = Console()
        self.language = {
            'python': ('.py', PythonLexer, '#'),
            'java': ('.java', JavaLexer, '//'),
            'javascript': ('.js', JavascriptLexer, '//'),
            'typescript': ('.ts', TypeScriptLexer, '//'),
        }

    def detect_language(self, language, folder_list: List[str]) -> str:
        language_extensions = {language[x][0]: [x, 0] for x in language}
        for folder in folder_list:
            for (_, _, files) in os.walk(folder, topdown=True):
                for file in files:
                    file_extension = os.path.splitext(file)[1]
                    if file_extension in language_extensions.keys():
                        count = language_extensions[file_extension][1] + 1
                        language_extensions[file_extension] = [language_extensions[file_extension][0], count]
        highest_count = 0
        language_detected = ''
        for language_extension in language_extensions.keys():
            if language_extensions[language_extension][1] > highest_count:
                highest_count = language_extensions[language_extension][1]
                language_detected = language_extensions[language_extension][0]
        return language_detected

    def generate_pdf(self):
        path = Prompt.ask('Please enter comma separated-list of folder(s) to scan')
        folder_list = path.split(sep=',')
        language_detected = self.detect_language(self.language, folder_list)
        data = ''
        for folder in folder_list:
            for (root, folder, files) in os.walk(folder, topdown=True):
                if '\\env\\' in root and language_detected == 'python':
                    continue
                for file in files:
                    if file.endswith(self.language[language_detected][0]):
                        data += f'\n\n{self.language[language_detected][2]} {root}/{file}\n\n'
                        with open(f'{root}/{file}', 'r') as file:
                            data += file.read()
        self.console.print(f'{language_detected} language detected, proceeding to generate pdf for code with highlighting')
        html = highlight(data, self.language[language_detected][1](), HtmlFormatter(full=True, linenos=True))
        pdfkit.from_string(html, 'out.pdf')
        self.open_file('out.pdf')
        self.console.print('PDF generation completed!')

    def open_file(self, filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
