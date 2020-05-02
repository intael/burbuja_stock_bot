from typing import List, Dict

from telegram.ext import CommandHandler
from datetime import date, datetime
import logging

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


def status(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Estoy vivito y coleando jeje"
    )


# TODO: Abstract out the details of this (arg parsing and validation, edge cases, etc).
# TODO: Support more than 1 date periods per ticker in the command handler. StocksDataRepository and the clients already do.
def stonks(update, context):
    stock_valuations: List[str] = context.args
    if len(stock_valuations) == 0:
        return context.bot.send_message(chat_id=update.effective_chat.id, text=STOCKS_COMMAND_FORMAT_ERROR_MESSAGE)
    message = SEPARATOR
    for stock_valuation in stock_valuations:
        try:
            components = stock_valuation.split(TICKER_COMPONENTS_SEPARATOR)
            ticker = components[0]
            if len(components) == 1:
                start_date, end_date = date.today(), date.today()
            else:
                period = components[1].split(PERIODS_SEPARATOR)
                start_date, end_date = (
                    datetime.strptime(period[0], "%Y%m%d").date(),
                    datetime.strptime(period[1], "%Y%m%d").date(),
                )
        except:
            return context.bot.send_message(chat_id=update.effective_chat.id, text=STOCKS_COMMAND_FORMAT_ERROR_MESSAGE)
        date_period = DatePeriod(start_date, end_date)
        try:
            valuations: Dict[
                DatePeriod, Valuation
            ] = stock_repository.get_stock_valuations(ticker, [date_period])
        except FinancialAPIUnavailableData:
            message += "No hay datos sobre este ticker: " + ticker + "\n"
            continue
        valuation: Valuation = valuations[date_period]
        message += "Ticker: " + ticker + "\n"
        message += (
            "Precio al inicio del periodo: "
            + str(round(valuation.starting_price, 2))
            + "\n"
        )
        message += (
            "Precio al final del periodo: " + str(round(valuation.end_price, 2)) + "\n"
        )
        message += (
            "Variación: {:.2%}".format(valuation.starting_price / valuation.end_price - 1)
            + "\n"
        )
    message += SEPARATOR
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


start_handler = CommandHandler("status", status)
stonk_handler = CommandHandler("stonks", stonks)
