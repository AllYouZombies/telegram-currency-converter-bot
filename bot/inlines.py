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
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=_('Click on the desired currency.'),
            description=_('Detailed information about the currency will be sent to the chat.'),
            input_message_content=InputTextMessageContent(
                _('Type <code>@%s</code> in any chat and enter the amount to convert.\n\nE.g.\n<code>@%s 100</code>')
                % (context.bot.username, context.bot.username),
                parse_mode=ParseMode.HTML
            ),
        )
    ]

    async def _create_article():
        exchange_rates = await ExchangeRate.get_rates(curr, BASE_CURR)  # All sources
        if not exchange_rates:
            return None
        cb_rate = sep(exchange_rates[0].rate)
        title = curr + ' (' + _('CB rate') + ': ' + cb_rate + ')'
        description = ''
        text = _('<b>%s %s</b> - exchange rates') % (sep(query), curr)
        text += _('\nCB rate: <b>%s</b>') % cb_rate
        text += _('\nSum: <b>%s</b>') % sep(query * exchange_rates[0].rate)
        best_buy = None
        best_sell = None
        best_buying_banks = set()
        best_selling_banks = set()
        for exchange_rate in exchange_rates:
            if exchange_rate.buy_rate and (not best_buy or exchange_rate.buy_rate > best_buy):
                best_buy = exchange_rate.buy_rate
                best_buying_banks = {exchange_rate.source}
            elif exchange_rate.buy_rate and exchange_rate.buy_rate == best_buy:
                best_buying_banks.add(exchange_rate.source)
            if exchange_rate.sell_rate and (not best_sell or exchange_rate.sell_rate < best_sell):
                best_sell = exchange_rate.sell_rate
                best_selling_banks = {exchange_rate.source}
            elif exchange_rate.sell_rate and exchange_rate.sell_rate == best_sell:
                best_selling_banks.add(exchange_rate.source)
        if best_buy:
            best_buy_str = _('➖ Best buy (bank buys)')
            rate_str = _('Rate')
            text += (f'\n\n----------\n\n'
                     f'<b>{best_buy_str}</b>'
                     f'\n{rate_str}: <b>{sep(best_buy)}</b> ({", ".join(best_buying_banks)})')
            text += _('\nSum: <b>%s</b>') % sep(query * best_buy)
            description += best_buy_str + ': ' + sep(best_buy)
        if best_sell:
            best_sell_str = _('➕ Best sell (bank sells)')
            rate_str = _('Rate')
            text += (f'\n\n----------\n\n'
                     f'<b>{best_sell_str}</b>'
                     f'\n{rate_str}: <b>{sep(best_sell)}</b> ({", ".join(best_selling_banks)})')
            text += _('\nSum: <b>%s</b>') % sep(query * best_sell)
            description += '\n' + best_sell_str + ': ' + sep(best_sell)
        if best_buy and best_sell:
            avg_str = _('⚖️ Average')
            rate_str = _('Rate')
            text += (f'\n\n----------\n\n'
                     f'<b>{avg_str}</b>'
                     f'\n{rate_str}: <b>{sep((best_buy + best_sell) / 2)}</b>')
            text += _('\nSum: <b>%s</b>') % sep(query * ((best_buy + best_sell) / 2))
        article = InlineQueryResultArticle(
            id=str(uuid4()),
            title=title,
            input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.HTML),
            description=description
        )
        results.append(article)

    for curr in SUPPORTED_CURRENCIES:
        await _create_article()

    await update.inline_query.answer(results, cache_time=0)
