import pytest

from arguments.validators.asset_valuation_argument_validator import (
    AssetPeriodValuationArgumentValidator,
)


@pytest.fixture
def asset_valuation_argument_validator_with_parameters(period_format: str):
    return AssetPeriodValuationArgumentValidator(period_format)
