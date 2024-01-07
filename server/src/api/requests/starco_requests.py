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
from src.utils.slug_utils import slugify

_base_url = env("STARCO_SERVICE_URL")
_username = env("STARCO_SERVICE_LOGIN")
_password = env("STARCO_SERVICE_PASSWORD")
basic_auth = HTTPBasicAuth(_username, _password)


def get_starco_tyres() -> list[StarcoTyreSchema]:
    unique_slugs = set()
    unique_tyres = []
    response = requests.get(
        f"{_base_url}/rus_product_catalog_tyres",
        auth=basic_auth,
    )
    parsed = response.json()
    tires = [StarcoTyreSchema(**tire) for tire in parsed["value"]]
    for tire in tires:
        slug = slugify(text=tire.full_name)
        if slug not in unique_slugs:
            tire.slug = slug
            unique_slugs.add(slug)
            unique_tyres.append(tire)
    return unique_tyres


def get_starco_rims() -> list[StarcoRimSchema]:
    unique_slugs = set()
    unique_rims = []
    response = requests.get(
        f"{_base_url}/rus_product_catalog_wheelsrims",
        auth=basic_auth,
    )
    parsed = response.json()
    rims = [StarcoRimSchema(**rim) for rim in parsed["value"]]
    for rim in rims:
        slug = slugify(text=rim.full_name)
        if slug not in unique_slugs:
            rim.slug = slug
            unique_slugs.add(slug)
            unique_rims.append(rim)
    return unique_rims


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
