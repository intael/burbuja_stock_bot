import pytest

from arguments.asset_valuation_argument import AssetValuationArgumentValidator


@pytest.fixture
def asset_valuation_argument_validator_with_parameters(
    argument: str, period_format: str
):
    return AssetValuationArgumentValidator(argument, period_format)
