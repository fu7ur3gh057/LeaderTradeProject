import os
from pathlib import Path
import urllib.request

import environ
import requests
from zeep import Client

from core.settings import WSDL_URL
from src.api.schemas.fortochki_schemas import (
    DiskPriceRestSchema,
    TyrePriceRestSchema,
    RimContainerSchema,
    TyreContainerSchema,
)

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, "../../.env"))

_base_url = env("4TOCHKI_SERVICE_URL")
_username = env("4TOCHKI_SERVICE_LOGIN")
_password = env("4TOCHKI_SERVICE_PASSWORD")
_client = Client(wsdl=WSDL_URL)


def refresh_wsdl_file() -> None:
    try:
        global _client
        urllib.request.urlretrieve(_base_url, WSDL_URL)
        print(f"Downloaded WSDL file from {_base_url} and saved it as {WSDL_URL}")
        _client = Client(wsdl=WSDL_URL)
    except Exception as e:
        print(f"Error: {e}")


def _get_tire_pages_count() -> int:
    global _client
    tires = _client.service.GetFindTyre(
        login=_username, password=_password, filter={"diameter_min": 14}
    )
    return int(tires.totalPages)


def find_rim_list() -> list[DiskPriceRestSchema]:
    global _client
    rim_list = []
    print("Finding Rims Data..")
    pages_count = None
    current_page = -1
    while pages_count is None or current_page < pages_count:
        current_page += 1
        if current_page == pages_count:
            break
        rims = _client.service.GetFindDisk(
            login=_username,
            password=_password,
            filter={"diameter_min": 14},
            page=current_page,
            pageSize=2000,
        )
        
        if pages_count == None:
            pages_count = int(rims.totalPages)

        for rim in rims.price_rest_list.DiskPriceRest:
            rim_schema = DiskPriceRestSchema.to_pydantic(data=rim)
            rim_list.append(rim_schema)


def find_tire_list() -> list[TyrePriceRestSchema]:
    global _client
    tire_list = []
    print("Finding Tires Data..")
    pages_count = None
    current_page = -1
    while pages_count is None or current_page < pages_count:
        current_page += 1
        if current_page == pages_count:
            break
        tires = _client.service.GetFindTyre(
            login=_username,
            password=_password,
            filter={"diameter_min": 14},
            page=current_page,
            pageSize=2000,
        )
        if pages_count == None:
            pages_count = int(tires.totalPages)
        for tire in tires.price_rest_list.TyrePriceRest:
            tire_schema = TyrePriceRestSchema.to_pydantic(data=tire)
            tire_list.append(tire_schema)
    return tire_list


def get_rim_goods_info(code_list: str) -> list[RimContainerSchema]:
    global _client
    result_list = []
    info_list = _client.service.GetGoodsInfo(
        login=_username, password=_password, code_list=code_list
    )
    for data in info_list.rimList.RimContainer:
        rim_schema = RimContainerSchema.to_pydantic(data=data)
        result_list.append(rim_schema)
    return result_list


def get_tire_goods_info(code_list: str) -> list[TyreContainerSchema]:
    global _client
    result_list = []
    info_list = _client.service.GetGoodsInfo(
        login=_username, password=_password, code_list=code_list
    )
    for data in info_list.tyreList.TyreContainer:
        tyre_schema = TyreContainerSchema.to_pydantic(data=data)
        result_list.append(tyre_schema)
    return result_list


def ¬(code_list: list[str]) -> str:
    global _client
    d_type = _client.get_type("ns3:ArrayOfstring")
    arr = d_type()
    for code in code_list:
        arr.string.append(code)
    return arr
