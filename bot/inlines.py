import logging
import re
from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from converter.models import ExchangeRate
from core.settings import SUPPORTED_CURRENCIES, BASE_CURR
from users.models import User
from utils.localization import activate_locale


log = logging.getLogger('inlines')


def sep(s, thou=" ", dec=".", digits=2):
    s = str(s)
    integer, decimal = s.split(dec)
    integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
    if int(decimal) == 0:
        return integer
    decimal = decimal[:digits]
    return f'{integer}{dec}{decimal}'


async def _inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle inline query.
    This method is called when user sends an inline query.
    It fetches exchange rates from the database and sends them to the user.

    :param update: Update instance
    :param context: Context instance
    """

    query = update.inline_query.query
    log.debug(f'Received inline query: {query}')
    log.debug(f'Checking user: {update.effective_user.id}')
    user = await User.from_update(update)
    lang = user.language_code
    log.debug(f'Activating user locale: {lang}')
    activate_locale(lang)

    if not query:
        query = 1
    try:
        query = float(query)
    except ValueError:
        return
    results = []

    async def _create_article():
        exchange_rates = await ExchangeRate.get_rates(curr, BASE_CURR)  # All sources
        if not exchange_rates:
            return None
        first_exchange_rate = exchange_rates[0]
        cb_rate = sep(first_exchange_rate.rate)
        cb_rate_str = _('CB rate')
        buying_str = _('Buying')
        selling_str = _('Selling')
        title = f'{curr} ({cb_rate_str}: {cb_rate})'
        text = f'<b>{sep(query)} {curr}</b>'
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
                    f' - {buying_str}: <b>{buying_converted}</b>\n'
                    f' - {selling_str}: <b>{selling_converted}</b>\n\n'
                )
            text += (
                f'1 {curr}:\n\n'
                f' - {buying_str}: <b>{buying}</b>\n'
                f' - {selling_str}: <b>{selling}</b>\n\n'
                f'---'
            )

        text += f'\n\n{cb_rate_str}: {cb_rate}\n\n'

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

    for curr in SUPPORTED_CURRENCIES:
        await _create_article()

    await update.inline_query.answer(results)
