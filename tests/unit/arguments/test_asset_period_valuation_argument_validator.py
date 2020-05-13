import pytest

from arguments.validators.invalid_argument_exception import InvalidArgument


@pytest.mark.parametrize(
    "argument", ["GOOG", "AMZN", "FB", "MSFT"],
)
@pytest.mark.parametrize("period_format", ["%Y%m%d"])
def test_validation_passes_when_input_contains_only_asset_id(
    asset_valuation_argument_validator_with_parameters, argument
):
    asset_valuation_argument_validator_with_parameters.validate(argument)


@pytest.mark.parametrize(
    "argument",
    ["GOOG:20200120-20200229", "AMZN:20100301-20110501", "FB:20150501-20200620"],
)
@pytest.mark.parametrize("period_format", ["%Y%m%d"])
def test_validation_passes_when_input_is_valid_with_format_ymd(
    asset_valuation_argument_validator_with_parameters, argument
):
    asset_valuation_argument_validator_with_parameters.validate(argument)


@pytest.mark.parametrize(
    "argument",
    [
        "GOOG:2020/01/20-2020/02/29",
        "AMZN:2010/03/01-2011/05/01",
        "FB:2015/05/01-2020/06/20",
    ],
)
@pytest.mark.parametrize("period_format", ["%Y/%m/%d"])
def test_validation_passes_when_input_is_valid_with_format_ymd_separated_by_slashes(
    asset_valuation_argument_validator_with_parameters, argument
):
    asset_valuation_argument_validator_with_parameters.validate(argument)


@pytest.mark.parametrize(
    "argument",
    [
        "GOOG:2020/01/20-2020/02/30",  # February the 30th does not exist because 2020 is a leap year
        "AMZN:2010/13/01-2011/05/01",  # 13 is not a valid month
        "FB:2015/05/01",  # Period end date is missing
        "GOOG:",  # Main component separator is present but period dates are missing
        "FB:2016/08/01-2016/01/01"  # period end is < period start
    ],
)
@pytest.mark.parametrize("period_format", ["%Y/%m/%d"])
def test_validation_fails_with_invalid_argument_exception_when_input_is_invalid_for_different_reasons(
    asset_valuation_argument_validator_with_parameters, argument
):
    with pytest.raises(InvalidArgument):
        asset_valuation_argument_validator_with_parameters.validate(argument)

