from arguments.validators.argument_validator import ArgumentValidator


class DatetimeValidatorInterface(ArgumentValidator):

    _datetime_period_format: str

    def get_datetime_period_format(self) -> str:
        return self._datetime_period_format
