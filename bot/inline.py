import datetime
import re
from html import escape
from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from converter.models import ExchangeRate
from core.settings import SUPPORTED_CURRENCIES, BASE_CURR


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if not query or not query.isdigit():  # empty query should not be handled
        return

    def sep(s, thou=" ", dec="."):
        integer, decimal = s.split(".")
        integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
        return integer + dec + decimal

    results = []

    for curr in SUPPORTED_CURRENCIES:

        exchange_rate = await ExchangeRate.get_rate(BASE_CURR, curr)
        exchange_rate_inverse = await ExchangeRate.get_rate(curr, BASE_CURR)

        result = float(query) / exchange_rate.rate
        conversion = sep("{0:.2f}".format(result))

        # rate_str = sep("{0:.8f}".format(exchange_rate.rate))
        inverse_str = sep("{0:.2f}".format(exchange_rate_inverse.rate))

        text = _(f'---\n<b>{datetime.date.today().strftime("%d.%m.%Y")}</b>\n---\n\n'
                 # f'1 {BASE_CURR} = {rate_str} {curr}\n\n'
                 f'1 {curr} = {inverse_str} {BASE_CURR}\n\n'
                 f'<b>{query} {curr} = {conversion} {BASE_CURR}</b>')

        description = _(f'{query} {curr} = {conversion} {BASE_CURR}\n'
                        f'1 {curr} = {inverse_str} {BASE_CURR}\n')

        article = InlineQueryResultArticle(
            id=str(uuid4()),
            title=curr,
            input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.HTML),
            description=description
        )
        results.append(article)

    await update.inline_query.answer(results)
