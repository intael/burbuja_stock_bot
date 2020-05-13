from datetime import date
from typing import Union

from arguments.parsed_argument import ParsedArgument


class AssetValuationArgument(ParsedArgument):

    _asset_id: str
    _period_start: date
    _period_end: date

    def __init__(self, asset_id: str, period_start: Union[date, None], period_end: Union[date, None]):
        self._asset_id = asset_id
        self._period_start = period_start
        self._period_end = period_end

    def get_asset_id(self) -> str:
        return self._asset_id

    def get_period_start(self) -> date:
        return self._period_start

    def get_period_end(self) -> date:
        return self._period_end
