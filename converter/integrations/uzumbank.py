import logging
import aiohttp
import json
from typing import Optional, List, Dict

from converter.integrations._base import ExchangeRateSource
from core.settings import BASE_CURR, SUPPORTED_CURRENCIES


async def convert_rate(rate_str: str) -> float:
    """
    Convert a rate string to a float. Replace commas with dots and remove non-breaking space.

    :param rate_str: Rate string.
    :return: Rate as float.
    """
    return float(rate_str.replace(',', '.').replace('\xa0', ''))


class UzumBank(ExchangeRateSource):
    source_name: str = 'Uzum Bank'
    endpoint: str = 'https://uzumbank.uz/api/currency'
    bulk: bool = True
    headers: Dict[str, str] = {'Host': 'uzumbank.uz'}

    def __init__(self) -> None:
        super().__init__()
        assert BASE_CURR == 'UZS', 'Uzum Bank only supports UZS as base currency.'

    async def _save_rate(self, exchange_rate_data: Dict[str, Optional[str]]) -> None:
        """
        Save exchange rate data to the database.

        :param exchange_rate_data: Dictionary containing iso_code, reval_rate, buy_rate, and sell_rate.
        """
        curr: str = exchange_rate_data.get('iso_code')
        rate_str = exchange_rate_data.get('reval_rate')
        rate: float = await convert_rate(rate_str) if rate_str else 0
        if rate == 1:
            return None
        buy_rate_str: Optional[str] = exchange_rate_data.get('buy_rate')
        buy_rate: Optional[float] = await convert_rate(buy_rate_str) if buy_rate_str else None
        sell_rate_str: Optional[str] = exchange_rate_data.get('sell_rate')
        sell_rate: Optional[float] = await convert_rate(sell_rate_str) if sell_rate_str else None
        rate_exists: bool = await self._check_existing(curr, BASE_CURR, rate, self.source_name, buy_rate, sell_rate)
        if rate_exists:
            return None
        await self.save_exchange_rate(curr, BASE_CURR, rate, self.source_name, buy_rate, sell_rate)

    async def get_rates(self) -> None:
        """
        Fetch exchange rates from Uzum Bank API and save them to the database.
        """
        async with aiohttp.ClientSession() as http_session:
            try:
                async with http_session.get(self.endpoint, headers=self.headers, timeout=5) as response:
                    response_text: str = await response.text()
                    assert response.status == 200, f'Uzum Bank returned {response.status} status code. {response_text}'
                    data: Dict[str, List[Dict[str, Optional[str]]]] = await response.json(encoding='utf-8')
            except Exception as e:
                logging.error(f'Cannot fetch exchange rates from Uzum Bank API. {e}')
                return None

        exchange_rate_data: List[Dict[str, Optional[str]]] = data.get('data')
        for data_point in exchange_rate_data:
            if data_point.get('iso_code') in SUPPORTED_CURRENCIES:
                await self._save_rate(data_point)
