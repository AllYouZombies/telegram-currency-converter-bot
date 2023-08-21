import asyncio

from converter.integrations.getgeoapi import GetGeoAPI
from converter.integrations.uzumbank import UzumBank
from core.celery import app


@app.task(ignore_result=True)
def retrieve_ggapi_exchange_rates():
    """
    Retrieve exchange rates from GetGeoAPI.
    """

    loop = asyncio.get_event_loop()

    loop.run_until_complete(GetGeoAPI().get_rates())


@app.task(ignore_result=True)
def retrieve_uzum_exchange_rates():
    """
    Retrieve exchange rates from Uzum Bank.
    """

    loop = asyncio.get_event_loop()

    loop.run_until_complete(UzumBank().get_rates())
