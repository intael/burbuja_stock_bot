from typing import List, Dict

from telegram.ext import CommandHandler
import logging

from arguments.asset_valuation_argument import AssetValuationArgument
from arguments.parsers.argument_parser_factory import ArgumentParserFactory
from arguments.validators.invalid_argument_exception import InvalidArgument
from src.finance.asset import Valuation
from src.finance.exceptions import FinancialAPIUnavailableData
from src.finance.repositories.client_factory import ClientFactory
from src.finance.repositories.stock_repositories import StocksDataRepository
from src.finance.time_range import DatePeriod

SEPARATOR = "<------------------------->\n"
TICKER_COMPONENTS_SEPARATOR = ":"
PERIODS_SEPARATOR = "-"
STOCKS_COMMAND_FORMAT_ERROR_MESSAGE = "Formato de petición inválido. El formato correcto es: /stonks TICKER1:FECHA1-FECHA2 TICKER2:FECHA3-FECHA4"

cmd_logger = logging.getLogger("main")
yahoo_client = ClientFactory.build(ClientFactory.YAHOO_CLIENT)
stock_repository = StocksDataRepository(yahoo_client)
stock_argument_parser = ArgumentParserFactory.build_asset_valuation_parser("%Y%m%d")

def status(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Estoy vivito y coleando jeje"
    )


# TODO: Abstract out the details of this (arg parsing and validation, edge cases, etc).
# TODO: Support more than 1 date periods per ticker in the command handler. StocksDataRepository and the clients already do.
def stonks(update, context):
    stock_valuations: List[str] = context.args
    message = SEPARATOR
    for stock_valuation in stock_valuations:
        try:
            valuation_argument: AssetValuationArgument = stock_argument_parser.parse(stock_valuation)
        except InvalidArgument:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=STOCKS_COMMAND_FORMAT_ERROR_MESSAGE,
            )
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
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


start_handler = CommandHandler("status", status)
stonk_handler = CommandHandler("stonks", stonks)
