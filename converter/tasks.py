import asyncio
import logging

import requests
from celery import shared_task

from converter.models import ExchangeRate
from core.celery import app
from core.db import session_scope
from core.settings import SUPPORTED_CURRENCIES, GETGEOAPI_KEY, BASE_CURR


@app.task()
def retrieve_exchage_rates():
    """Retrieve exchange rates from the API and save them to the database."""

    for curr in SUPPORTED_CURRENCIES:
        retrieve_currency_rate.delay(curr)


@shared_task()
def retrieve_currency_rate(curr: str):
    """
    Retrieve the exchange rate for the given currency.

    :param curr: The currency to retrieve the exchange rate for.
    """

    parameters = {
        "api_key": GETGEOAPI_KEY,
        "format": "json",
        "from": curr,
        "to": BASE_CURR,
        "amount": 1
    }
    url = "https://api.getgeoapi.com/v2/currency/convert"

    try:
        response = requests.get(url, parameters)
    except requests.exceptions.RequestException as e:
        logging.error(e.__str__())
        return None
    data = response.json()
    rate = data["rates"][BASE_CURR]["rate"]

    rate = float(rate)
    inverse = "{0:.10f}".format(1 / rate)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_exchange_rate(curr, BASE_CURR, rate))
    loop.run_until_complete(save_exchange_rate(BASE_CURR, curr, inverse))


async def save_exchange_rate(from_curr: str, to_curr: str, rate: str | float | int):
    """
    Save the exchange rate for the given currencies to the database.

    :param from_curr: The currency to convert from.
    :param to_curr: The currency to convert to.
    :param rate: The exchange rate.
    """

    async with session_scope() as session:
        exchange_rate = ExchangeRate(from_currency=from_curr, to_currency=to_curr, rate=float(rate))
        session.add(exchange_rate)
