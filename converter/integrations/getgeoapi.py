import aiohttp

from converter.integrations._base import ExchangeRateSource, save_exchange_rate
from core.settings import GETGEOAPI_KEY, SUPPORTED_CURRENCIES, BASE_CURR


class GetGeoAPI(ExchangeRateSource):
    source_name = 'GetGeoAPI'
    endpoint = 'https://api.getgeoapi.com/v2/currency/convert'
    bulk = False
    coef = 10000

    async def get_params(self, from_curr: str, to_curr: str) -> dict:
        params = {
            "api_key": GETGEOAPI_KEY,
            "format": "json",
            "from": from_curr,
            "to": to_curr,
            "amount": self.coef
        }
        return params

    async def get_rates(self):
        for curr in SUPPORTED_CURRENCIES:
            params = await self.get_params(curr, BASE_CURR)
            await self.get_rate(curr, BASE_CURR, params)

    async def get_rate(self, from_currency: str | float | int, to_currency: str | float | int, params: dict = None):

        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(self.endpoint, params=params) as response:
                response_text = await response.text()
                assert response.status == 200, f'GetGeoAPI returned {response.status} status code. {response_text}'
                data = await response.json()

        rate = data["rates"][to_currency]["rate_for_amount"]
        rate = float(rate) / self.coef
        if rate > 1:
            rate = '{:.2f}'.format(rate)
        rate_exists = await self._check_existing(from_currency, to_currency, rate, rate, rate)
        if rate_exists:
            return
        await save_exchange_rate(from_currency, to_currency, rate, source=self.source_name)
