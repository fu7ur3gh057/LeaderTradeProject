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


def _get_tire_total_pages() -> int:
    tires = _client.service.GetFindTyre(
        login=_username, password=_password, filter={"diameter_min": 14}
    )
    return int(tires.totalPages)


def _get_rim_total_pages() -> int:
    disks = _client.service.GetFindDisk(
        login=_username, password=_password, filter={"diameter_min": 14}
    )
    return int(disks.totalPages)


def find_rim_list() -> list[DiskPriceRestSchema]:
    rim_list = []
    total_pages = _get_rim_total_pages()
    for _ in range(total_pages):
        rims = _client.service.GetFindDisk(
            login=_username,
            password=_password,
            filter={"diameter_min": 14},
            page=_,
            pageSize=50,
        )
        for rim in rims.price_rest_list.DiskPriceRest:
            rim_schema = DiskPriceRestSchema.to_pydantic(data=rim)
            rim_list.append(rim_schema)
    return rim_list


def find_tire_list() -> list[TyrePriceRestSchema]:
    tire_list = []
    total_pages = _get_tire_total_pages()
    for _ in range(total_pages):
        tires = _client.service.GetFindTyre(
            login=_username,
            password=_password,
            filter={"diameter_min": 14},
            page=_,
            pageSize=50,
        )
        for tire in tires.price_rest_list.TyrePriceRest:
            tire_schema = TyrePriceRestSchema.to_pydantic(data=tire)
            tire_list.append(tire_schema)
    return tire_list


def get_rim_goods_info(code_list: str) -> list[RimContainerSchema]:
    result_list = []
    info_list = _client.service.GetGoodsInfo(
        login=_username, password=_password, code_list=code_list
    )
    for data in info_list.rimList.RimContainer:
        rim_schema = RimContainerSchema.to_pydantic(data=data)
        result_list.append(rim_schema)
    return result_list


def get_tire_goods_info(code_list: str) -> list[TyreContainerSchema]:
    result_list = []
    info_list = _client.service.GetGoodsInfo(
        login=_username, password=_password, code_list=code_list
    )
    for data in info_list.tyreList.TyreContainer:
        tyre_schema = TyreContainerSchema.to_pydantic(data=data)
        result_list.append(tyre_schema)
    return result_list


def convert_code_list(code_list: list[str]) -> str:
    d_type = _client.get_type("ns3:ArrayOfstring")
    arr = d_type()
    for code in code_list:
        arr.string.append(code)
    return arr
