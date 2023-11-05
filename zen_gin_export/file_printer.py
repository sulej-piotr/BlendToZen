from .printer import Printer


class FilePrinter(Printer):
    __content = ""

    def __init__(self, filepath):
        self.__filepath = filepath

    def __del__(self):
        with open(self.__filepath, 'w') as file:
            print(self.__content, end="", file=file)

    def print(self, *content):
        for content_part in content:
            self.__content = self.__content + content_part
        self.__content = self.__content + "\n"
