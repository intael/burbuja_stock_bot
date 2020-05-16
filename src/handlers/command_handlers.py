from typing import List
import re

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler
import logging

from handlers.value_handler import value_handler_broker

VALUE_COMMAND_REGEX_TOKEN = "[$]([a-zA-Z]+)"
VALUE_BY_TOKEN_COMMAND_REGEX_TOKEN = "[$]([a-zA-Z]+[:][0-9]{8}-[0-9]{8})"

cmd_logger = logging.getLogger("main")


def status(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Estoy vivito y coleando jeje"
    )


# TODO: The logic of the 2 regex is really shabby, see if it can be handled more elegantly
def value_by_token(update, context):
    message = update.message.text
    period_asset_valuation = re.findall(VALUE_BY_TOKEN_COMMAND_REGEX_TOKEN, message)
    todays_asset_valuation = re.findall(VALUE_COMMAND_REGEX_TOKEN, message)
    for period in period_asset_valuation:
        todays_asset_valuation = [asset_id for asset_id in todays_asset_valuation if asset_id not in period]
    matches = period_asset_valuation + todays_asset_valuation
    if len(matches) > 0:
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        message = value_handler_broker(matches)
        update.message.reply_text(message, parse_mode=telegram.ParseMode.MARKDOWN)


# TODO: Support more than 1 date periods per asset ID in the command handler. StocksDataRepository and the clients already do.
def value(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    asset_valuations: List[str] = context.args
    message = value_handler_broker(asset_valuations)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


start_handler = CommandHandler("status", status)
value_handler = CommandHandler("value", value)
token_query_handler = MessageHandler(filters=Filters.text & (~Filters.command), callback=value_by_token)
