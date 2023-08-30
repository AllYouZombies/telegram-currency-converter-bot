import datetime
import logging
import re

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import select, Date, cast, delete

from converter.integrations._base import ExchangeRateSource
from converter.models import ExchangeRate
from core.db import session_scope
from core.settings import BASE_CURR, SUPPORTED_CURRENCIES

log = logging.getLogger('integrations.pultop')


class Pultop(ExchangeRateSource):
    endpoint = 'https://pultop.uz/kurs-obmena-valyut/'

    def __init__(self) -> None:
        super().__init__()
        assert BASE_CURR == 'UZS', 'Pultop only supports UZS as base currency.'

    async def get_rates(self) -> None:
        async def _get_best_values(column):
            best_value = column.find(string=True, recursive=False).strip()
            best_value = _format_currency_value(best_value)
            best_value_hidden_block = column.find_all('div', class_='best-kurs-item')
            if len(best_value_hidden_block) > 0:
                best_value_banks = list(bank.text.strip() for bank in best_value_hidden_block)
            else:
                best_value_banks = [column.find('div', class_='best-kurs-block').text.strip()]
            return best_value, best_value_banks

        def _format_currency_value(value):
            pattern = r"[\d,.]+"
            matches = re.findall(pattern, value)
            formatted_string = ''.join(matches).replace(',', '.')
            result = float(formatted_string)
            return result

        async def _parse_row(input_row):
            columns = input_row.find_all('td')
            currency = columns[0].find('span').text
            if currency not in SUPPORTED_CURRENCIES:
                return None
            best_buy, best_buying_banks = await _get_best_values(columns[1])
            best_sell, best_selling_banks = await _get_best_values(columns[2])
            cb_rate = _format_currency_value(columns[3].text.strip())
            actual_rate_banks = set(best_buying_banks + best_selling_banks)
            async with session_scope() as db_session:
                existig_rate_banks = await db_session.execute(select(ExchangeRate).filter(
                    cast(ExchangeRate.created_at, Date) == datetime.date.today()
                ))
                existig_rate_banks = set(rate.bank_name for rate in existig_rate_banks.scalars().all())
            for bank_name in actual_rate_banks:
                buy_rate = best_buy if bank_name in best_buying_banks else None
                sell_rate = best_sell if bank_name in best_selling_banks else None
                rate_exists = await self._check_existing(currency, BASE_CURR, cb_rate, bank_name, buy_rate, sell_rate)
                if rate_exists:
                    continue
                if bank_name not in existig_rate_banks:
                    async with session_scope() as db_session:
                        await db_session.execute(delete(ExchangeRate).filter(
                            cast(ExchangeRate.created_at, Date) == datetime.date.today(),
                            ExchangeRate.source == self.source_name,
                            ExchangeRate.bank_name == bank_name
                        ))
                await self.save_exchange_rate(currency, BASE_CURR, cb_rate, bank_name, buy_rate, sell_rate)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint, ssl=False) as response:
                if not response.status == 200:
                    log.error(f'Error {response.status} {response.reason}')
                    return None
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                table = soup.find('table', class_='best-kurs-table')
                rows = table.find_all('tr')
                for row in rows:
                    await _parse_row(row)
