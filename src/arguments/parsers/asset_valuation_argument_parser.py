from datetime import date, datetime
from typing import List

from arguments.asset_valuation_argument import AssetValuationArgument
from arguments.parsers.argument_parser import ArgumentParser
from arguments.utils import split_components
from arguments.validators.datetime_validator_interface import DatetimeValidatorInterface


class AssetValuationArgumentParser(ArgumentParser):
    MAIN_COMPONENTS_SEPARATOR = ":"
    TIME_PERIOD_SEPARATOR = "-"

    validator: DatetimeValidatorInterface

    def __init__(self, validator: DatetimeValidatorInterface):
        """The validator dependency needs to provide have a datetime_period_format property"""
        self.validator = validator

    def parse(self, argument: str) -> AssetValuationArgument:
        """
        Parses a request argument into an AssetValuationArgument. If there is no period in the request, we make the period the current UTC date.
        :param argument:
        :return:
        :raise: InvalidArgument
        """
        self.validator.validate(argument)
        components = split_components(
            argument, AssetValuationArgumentParser.MAIN_COMPONENTS_SEPARATOR
        )
        if AssetValuationArgumentParser.MAIN_COMPONENTS_SEPARATOR in argument:
            time_period: List[str] = split_components(
                components[1], AssetValuationArgumentParser.TIME_PERIOD_SEPARATOR
            )
            period_start: date = self._parse_datetime_string(time_period[0]).date()
            period_end: date = self._parse_datetime_string(time_period[1]).date()
        else:
            period_start, period_end = (
                datetime.utcnow().date(),
                datetime.utcnow().date(),
            )
        asset_valuation = AssetValuationArgument(
            components[0], period_start, period_end
        )
        return asset_valuation

    def _parse_datetime_string(self, datetime_string: str) -> datetime:
        return datetime.strptime(
            datetime_string, self.validator.get_datetime_period_format()
        )
