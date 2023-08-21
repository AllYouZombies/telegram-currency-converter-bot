import logging
from datetime import datetime

import aiohttp
from sqlalchemy import cast, Date, select

from converter.integrations._base import ExchangeRateSource, save_exchange_rate
from converter.models import ExchangeRate
from core.db import session_scope
from core.settings import BASE_CURR, SUPPORTED_CURRENCIES


class UzumBank(ExchangeRateSource):
    source_name = 'Uzum Bank'
    endpoint = 'https://uzumbank.uz/api/currency'
    bulk = True
    headers = {'Host': 'uzumbank.uz'}

    def __init__(self):
        super().__init__()
        assert BASE_CURR == 'UZS', 'Uzum Bank only supports UZS as base currency.'

    async def get_rates(self):
        async with aiohttp.ClientSession() as http_session:
            try:
                async with http_session.get(self.endpoint, headers=self.headers, timeout=5) as response:
                    response_text = await response.text()
                    assert response.status == 200, f'Uzum Bank returned {response.status} status code. {response_text}'
                    data = await response.json(encoding='utf-8')
            except Exception as e:
                logging.error(e.__str__())
                return None
        data = data.get('data')
        for rate_obj in data:
            if not rate_obj.get('iso_code') in SUPPORTED_CURRENCIES:
                continue

            curr = rate_obj.get('iso_code')

            rate_str = rate_obj.get('reval_rate')
            rate_str = rate_str.replace(',', '.').replace('\xa0', '')
            rate = float(rate_str)
            if rate == 1:
                continue
            buy_rate_str = rate_obj.get('buy_rate')
            buy_rate_str = buy_rate_str.replace(',', '.').replace('\xa0', '')
            buy_rate = float(buy_rate_str) if buy_rate_str else None
            sell_rate_str = rate_obj.get('sell_rate')
            sell_rate_str = sell_rate_str.replace(',', '.').replace('\xa0', '')
            sell_rate = float(sell_rate_str) if sell_rate_str else None
            rate_exists = await self._check_existing(curr, BASE_CURR, rate, buy_rate, sell_rate)
            if rate_exists:
                continue
            await save_exchange_rate(curr, BASE_CURR, rate,
                                     source=self.source_name, buy_rate=buy_rate, sell_rate=sell_rate)
