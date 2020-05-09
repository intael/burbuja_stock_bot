from abc import ABC, abstractmethod


class ArgumentValidator(ABC):
    @abstractmethod
    def validate(self) -> None:
        """Throws an InvalidArgument exception if the argument is invalid."""
        pass
