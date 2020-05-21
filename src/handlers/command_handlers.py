from typing import List

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler
import logging

from handlers.token_matching import match_token
from handlers.value_handler import value_handler_broker

WHITESPACE_STRING = " "
cmd_logger = logging.getLogger("main")


def status(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Estoy vivito y coleando jeje"
    )


def value_by_token(update, context):
    matches = set()
    for word in update.message.text.split(WHITESPACE_STRING):
        match = match_token(word)
        if match is not None:
            matches.add(match)
    if len(matches) > 0:
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        message = value_handler_broker(list(matches))
        update.message.reply_text(message, parse_mode=telegram.ParseMode.MARKDOWN)


# TODO: Support more than 1 date periods per asset ID in the command handler. StocksDataRepository and the clients already do.
def value(update, context):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
    )
    asset_valuations: List[str] = context.args
    message = value_handler_broker(asset_valuations)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


start_handler = CommandHandler("status", status)
value_handler = CommandHandler("value", value)
token_query_handler = MessageHandler(
    filters=Filters.text & (~Filters.command), callback=value_by_token
)
