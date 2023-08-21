import datetime
import re
from html import escape
from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from converter.models import ExchangeRate
from core.settings import SUPPORTED_CURRENCIES, BASE_CURR
from users.models import User
from utils.localization import activate_locale


def sep(s, thou=" ", dec=".", digits=2):
    s = str(s)
    integer, decimal = s.split(dec)
    integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
    if int(decimal) == 0:
        return integer
    decimal = decimal[:digits]
    return f'{integer}{dec}{decimal}'


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    user = await User.from_update(update)
    lang = user.language_code
    activate_locale(lang)

    if not query:
        query = 1
    try:
        query = float(query)
    except ValueError:
        return
    results = []

    for curr in SUPPORTED_CURRENCIES:
        exchange_rates = await ExchangeRate.get_rates(curr, BASE_CURR)  # All sources
        if not exchange_rates:
            continue
        first_exchange_rate = exchange_rates[0]
        cb_rate = sep(first_exchange_rate.rate)
        cb_rate_str = _('CB rate')
        buying_str = _('Buying')
        selling_str = _('Selling')
        title = f'{curr} ({cb_rate_str}: {cb_rate})'
        text = f'🗓️ <b>{datetime.date.today().strftime("%d.%m.%Y")}</b>'
        for exchange_rate in exchange_rates:
            buying = sep(exchange_rate.buy_rate)
            selling = sep(exchange_rate.sell_rate)
            buying_converted = sep(exchange_rate.buy_rate * query)
            selling_converted = sep(exchange_rate.sell_rate * query)
            text += (
                f'\n\n---\n\n'
                f'🏦 <b>{exchange_rate.source} ({exchange_rate.created_at.strftime("%d.%m.%Y")})</b>\n\n'
            )
            if query != 1:
                text += (
                    f'<b>{sep(query)} {curr}</b>\n\n'
                    f' - {buying_str}: <b>{buying_converted}</b>\n'
                    f' - {selling_str}: <b>{selling_converted}</b>\n\n'
                )
            text += (
                f'<b>1 {curr}</b>\n\n'
                f' - {buying_str}: <b>{buying}</b>\n'
                f' - {selling_str}: <b>{selling}</b>\n\n'
                f'---\n\n'
                f'{cb_rate_str}: {cb_rate}\n\n'
            )

        description = (f'{buying_str}: {sep(first_exchange_rate.buy_rate)} '
                       f'({first_exchange_rate.source})\n'
                       f'{selling_str}: {sep(first_exchange_rate.sell_rate)} '
                       f'({first_exchange_rate.source})')

        article = InlineQueryResultArticle(
            id=str(uuid4()),
            title=title,
            input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.HTML),
            description=description
        )
        results.append(article)

    await update.inline_query.answer(results)
