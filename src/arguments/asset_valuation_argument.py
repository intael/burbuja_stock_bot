from arguments.argument_validator import ArgumentValidator
from arguments.invalid_argument_exception import InvalidArgument
from typing import Type, List
from datetime import datetime


class AssetValuationArgumentValidator(ArgumentValidator):
    """Validates strings with the format: NAME:TIME_PERIOD1-TIME_PERIOD2. The time periods must
    conform to a provided format according to the python datetime library. See this for more detail:
    https://docs.python.org/3.8/library/datetime.html#strftime-strptime-behavior
    """

    MAIN_COMPONENTS_SEPARATOR = ":"
    EXPECTED_MAIN_COMPONENTS = 2
    TIME_PERIOD_SEPARATOR = "-"
    EXPECTED_PERIOD_COMPONENTS = 2
    TICKER_FIELD = "ticker"
    START_TIME = "start_time"
    END_TIME = "end_time"

    raw_argument: str
    time_period_format: str
    main_components: Type[tuple]
    validated_period_start: datetime
    validated_period_end: datetime
    asset_id: str

    def __init__(self, raw_argument: str, time_period_format: str):
        self.raw_argument = raw_argument
        self.time_period_format = time_period_format

    def validate(self) -> None:
        if not isinstance(self.raw_argument, str) or len(self.raw_argument) == 0:
            raise InvalidArgument(self.raw_argument)
        if (
            AssetValuationArgumentValidator.MAIN_COMPONENTS_SEPARATOR
            in self.raw_argument
        ):
            components = self._split_components(
                self.raw_argument,
                AssetValuationArgumentValidator.MAIN_COMPONENTS_SEPARATOR,
                AssetValuationArgumentValidator.EXPECTED_MAIN_COMPONENTS,
            )
            self._validate_asset_id(components[0])
            self.asset_id = components[0]
            time_periods = self._split_components(
                components[1],
                AssetValuationArgumentValidator.TIME_PERIOD_SEPARATOR,
                AssetValuationArgumentValidator.EXPECTED_PERIOD_COMPONENTS,
            )
            self.validated_period_start = self._validate_date_periods(time_periods[0])
            self.validated_period_end = self._validate_date_periods(time_periods[1])
            self._validate_period_start_is_before_period_end()
        else:
            self._validate_asset_id(self.raw_argument)
            self.asset_id = self.raw_argument

    def _split_components(
        self, components_string: str, separator: str, expected_components: int
    ) -> List[str]:
        components = components_string.split(separator)
        if len(components) != expected_components:
            raise InvalidArgument(self.raw_argument)
        return components

    def _validate_date_periods(self, time_period_string: str) -> datetime:
        try:
            return datetime.strptime(time_period_string, self.time_period_format)
        except ValueError:
            raise InvalidArgument(self.raw_argument)

    def _validate_period_start_is_before_period_end(self):
        if self.validated_period_start > self.validated_period_end:
            raise InvalidArgument(self.raw_argument)

    def _validate_asset_id(self, asset_id_string: str):
        if len(asset_id_string) == 0:
            raise InvalidArgument(self.raw_argument)
