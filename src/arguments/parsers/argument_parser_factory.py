from arguments.parsers.argument_parser import ArgumentParser
from arguments.parsers.asset_valuation_argument_parser import (
    AssetValuationArgumentParser,
)
from arguments.validators.argument_validator_factory import ArgumentValidatorFactory
from arguments.validators.datetime_validator_interface import DatetimeValidatorInterface


class ArgumentParserFactory:
    ARGUMENT_VALIDATORS = {AssetValuationArgumentParser}

    @staticmethod
    def build_asset_valuation_parser(datetime_format: str) -> ArgumentParser:
        validator: DatetimeValidatorInterface = ArgumentValidatorFactory.build_asset_valuation_argument_validator(
            datetime_format
        )
        return AssetValuationArgumentParser(validator)
