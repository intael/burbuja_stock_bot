from abc import ABC, abstractmethod

from arguments.parsed_argument import ParsedArgument


class ArgumentParser(ABC):
    @abstractmethod
    def parse(self, argument: str) -> ParsedArgument:
        """
        Converts a raw argument to a specific type. Throws ArgumentParsingException if something goes wrong while
        parsing.
        :param argument:
        :return:
        """
        pass
