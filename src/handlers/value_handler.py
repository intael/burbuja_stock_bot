from typing import List, Dict

from arguments.asset_valuation_argument import AssetValuationArgument
from arguments.parsers.argument_parser_factory import ArgumentParserFactory
from arguments.validators.invalid_argument_exception import InvalidArgument
from finance.asset import Valuation
from finance.exceptions import FinancialAPIUnavailableData
from finance.repositories.client_factory import ClientFactory
from finance.repositories.stock_repositories import StocksDataRepository
from finance.time_range import DatePeriod

SEPARATOR = "<------------------------->\n"
TICKER_COMPONENTS_SEPARATOR = ":"
PERIODS_SEPARATOR = "-"
STOCKS_COMMAND_FORMAT_ERROR_MESSAGE = "Formato de petición inválido. El formato correcto es: /stonks TICKER1:FECHA1-FECHA2 TICKER2:FECHA3-FECHA4"

yahoo_client = ClientFactory.build(ClientFactory.YAHOO_CLIENT)
stock_repository = StocksDataRepository(yahoo_client)
stock_argument_parser = ArgumentParserFactory.build_asset_valuation_parser("%Y%m%d")


def value_handler_broker(asset_valuations: List[str]) -> str:
    message = SEPARATOR
    for stock_valuation in asset_valuations:
        try:
            valuation_argument: AssetValuationArgument = stock_argument_parser.parse(stock_valuation)
        except InvalidArgument:
            return STOCKS_COMMAND_FORMAT_ERROR_MESSAGE
        date_period = DatePeriod(valuation_argument.get_period_start(), valuation_argument.get_period_end())
        try:
            valuations: Dict[
                DatePeriod, Valuation
            ] = stock_repository.get_stock_valuations(valuation_argument.get_asset_id(), [date_period])
        except FinancialAPIUnavailableData:
            message += "No hay datos sobre este ticker: " + valuation_argument.get_asset_id() + "\n"
            continue
        valuation: Valuation = valuations[date_period]
        message += "Ticker: " + valuation_argument.get_asset_id() + "\n"
        message += (
            "Precio al inicio del periodo: "
            + str(round(valuation.starting_price, 2))
            + "\n"
        )
        message += (
            "Precio al final del periodo: " + str(round(valuation.end_price, 2)) + "\n"
        )
        message += (
            "Variación: {:.2%}".format(
                valuation.end_price / valuation.starting_price - 1
            )
            + "\n"
        )
    message += SEPARATOR
    return message
