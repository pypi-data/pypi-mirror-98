from typing import List
from consolebundle.ConsoleCommand import ConsoleCommand


class CommandManager:
    def __init__(self, commands: List[ConsoleCommand]):
        self.__commands = commands

    def get_commands(self):
        return self.__commands

    def get_by_name(self, name: str) -> ConsoleCommand:
        for command in self.__commands:
            if command.get_command() == name:
                return command

        raise Exception('No command with name "{}" found'.format(name))
