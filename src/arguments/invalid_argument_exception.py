class InvalidArgument(Exception):
    def __init__(self, argument: str):
        self.argument = argument

    def __repr__(self):
        return f"The provided argument {self.argument} is invalid."
