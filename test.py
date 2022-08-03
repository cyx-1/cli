from cli import CLI, Weather, Clipboard, CodePDFGenerator

cli = CLI(Weather(), Clipboard(), CodePDFGenerator())
cli.start()
