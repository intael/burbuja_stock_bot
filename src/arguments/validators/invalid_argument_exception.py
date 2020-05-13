class InvalidArgument(Exception):
    def __init__(self, argument: str):
        self.argument = argument

    def __repr__(self):
        return f"The provided argument {self.argument} is invalid."


class InvalidArgumentComponent(InvalidArgument):
    def __init__(self, component_name: str, component: str):
        self.component_name = component_name
        self.component = component

    def __repr__(self):
        return f"The provided argument is invalid due to the {self.component_name} having an invalid value {self.component}."


class InvalidPeriodArgumentLogic(InvalidArgument):
    def __init__(self, period_start: str, period_end: str):
        self.period_start = period_start
        self.period_end = period_end

    def __repr__(self):
        return f"The provided period argument is invalid. Check the start and end datetimes: Start={self.period_start}, End={self.period_end}"
