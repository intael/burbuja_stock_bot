from arguments.utils import split_components
from arguments.validators.datetime_validator_interface import DatetimeValidatorInterface
from arguments.validators.invalid_argument_exception import (
    InvalidArgument,
    InvalidArgumentComponent,
    InvalidPeriodArgumentLogic,
)
from datetime import datetime


class AssetPeriodValuationArgumentValidator(DatetimeValidatorInterface):
    """Validates strings with the format: NAME:TIME_PERIOD1-TIME_PERIOD2. The time periods must
    conform to a provided format according to the python datetime library. See this for more detail:
    https://docs.python.org/3.8/library/datetime.html#strftime-strptime-behavior
    """

    MAIN_COMPONENTS_SEPARATOR = ":"
    EXPECTED_MAIN_COMPONENTS = 2
    TIME_PERIOD_SEPARATOR = "-"
    EXPECTED_PERIOD_COMPONENTS = 2

    def __init__(self, datetime_period_format: str):
        self._datetime_period_format = datetime_period_format

    def validate(self, argument: str) -> None:
        if not isinstance(argument, str) or len(argument) == 0:
            raise InvalidArgument(argument)
        if AssetPeriodValuationArgumentValidator.MAIN_COMPONENTS_SEPARATOR in argument:
            components = split_components(
                argument,
                AssetPeriodValuationArgumentValidator.MAIN_COMPONENTS_SEPARATOR,
                AssetPeriodValuationArgumentValidator.EXPECTED_MAIN_COMPONENTS,
            )
            self._validate_asset_id(components[0])
            time_periods = split_components(
                components[1],
                AssetPeriodValuationArgumentValidator.TIME_PERIOD_SEPARATOR,
                AssetPeriodValuationArgumentValidator.EXPECTED_PERIOD_COMPONENTS,
            )
            period_start = self._validate_date_periods(time_periods[0])
            period_end = self._validate_date_periods(time_periods[1])
            self._validate_period_start_is_before_period_end(period_start, period_end)
        else:
            self._validate_asset_id(argument)

    def _validate_date_periods(self, datetime_string: str) -> datetime:
        try:
            return datetime.strptime(datetime_string, self._datetime_period_format)
        except ValueError:
            raise InvalidArgumentComponent("valuation period", datetime_string)

    def _validate_period_start_is_before_period_end(
        self, period_start: datetime, period_end: datetime
    ):
        if period_start > period_end:
            raise InvalidPeriodArgumentLogic(str(period_start), str(period_end))

    def _validate_asset_id(self, asset_id_string: str):
        if len(asset_id_string) == 0:
            raise InvalidArgument(asset_id_string)
