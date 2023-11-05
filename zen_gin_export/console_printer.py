from .printer import Printer


class ConsolePrinter(Printer):

    def print(self, *content):
        print(*content)
