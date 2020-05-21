import re
from typing import Union

VALUE_COMMAND_REGEX_TOKEN = "[$]([a-zA-Z]+$)"
VALUE_BY_TOKEN_COMMAND_REGEX_TOKEN = "[$]([a-zA-Z]+[:][0-9]{8}-[0-9]{8})"


def match_token(message_word: str) -> Union[str, None]:
    period_asset_valuation = re.findall(
        VALUE_BY_TOKEN_COMMAND_REGEX_TOKEN, message_word
    )
    if len(period_asset_valuation) > 0:
        return period_asset_valuation[0]  # Only 1 token per word is accepted
    todays_asset_valuation = re.findall(VALUE_COMMAND_REGEX_TOKEN, message_word)
    if len(todays_asset_valuation) > 0:
        return todays_asset_valuation[0]
    return None
