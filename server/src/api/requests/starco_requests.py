import os
from pathlib import Path

import environ
import requests
from requests.auth import HTTPBasicAuth

from src.api.schemas.starco_schemas import (
    StarcoTyreSchema,
    StarcoRimSchema,
    StarcoStockSchema,
    StarcoPriceSchema,
)

from core.settings import env

_base_url = env("STARCO_SERVICE_URL")
_username = env("STARCO_SERVICE_LOGIN")
_password = env("STARCO_SERVICE_PASSWORD")
basic_auth = HTTPBasicAuth(_username, _password)


def get_starco_tyres() -> list[StarcoTyreSchema]:
    response = requests.get(
        f"{_base_url}/rus_product_catalog_tyres",
        auth=basic_auth,
    )
    parsed = response.json()
    tires = [StarcoTyreSchema(**tire) for tire in parsed["value"]]
    return tires


def get_starco_rims() -> list[StarcoRimSchema]:
    response = requests.get(
        f"{_base_url}/rus_product_catalog_wheelsrims",
        auth=basic_auth,
    )
    parsed = response.json()
    rims = [StarcoRimSchema(**rim) for rim in parsed["value"]]
    return rims


def get_starco_stock() -> list[StarcoStockSchema]:
    response = requests.get(f"{_base_url}/current_stock_full", auth=basic_auth)
    parsed = response.json()
    stocks = [StarcoStockSchema(**stock) for stock in parsed["value"]]
    return stocks


def get_starco_prices() -> list[StarcoPriceSchema]:
    response = requests.get(f"{_base_url}/120184_pl", auth=basic_auth)
    parsed = response.json()
    price_list = [StarcoPriceSchema(**price) for price in parsed["value"]]
    return price_list
