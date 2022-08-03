# cli test usage
- create a virtual environment, active it
- pip install from requirements.in: python -m pip install -r requirements.in
- run the test.py program: python test.py
- see: https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf if "code to pdf" command is needed

# cli library usage
- the following is useful if cli is used as a library
- create a new project with its own virtual env (python -m pip venv env)
- activate virtual environment
- traverse to the cli project folder and install cli package and its dependencies (python setup.py develop)
- create a file like below in the new project folder
```
from cli import CLI, Weather, Clipboard, SecondBrain
cli = CLI(Weather(), Clipboard())
cli.start()
```
- run the program
- following the steps above would link the new project to the CLI folder, any code change in the CLI folder will reflect automatically