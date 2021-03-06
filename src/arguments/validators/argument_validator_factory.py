from arguments.validators.asset_valuation_argument_validator import (
    AssetPeriodValuationArgumentValidator,
)


class ArgumentValidatorFactory:
    ARGUMENT_VALIDATORS = {AssetPeriodValuationArgumentValidator}

    @staticmethod
    def build_asset_valuation_argument_validator(datetime_format: str):
        return AssetPeriodValuationArgumentValidator(datetime_format)
