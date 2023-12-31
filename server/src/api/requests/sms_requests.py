import os
from pathlib import Path

import environ
import requests

from core.settings import env

_username = env("SMS_SERVICE_LOGIN")
_password = env("SMS_SERVICE_PASSWORD")
_base_url = env("SMS_SERVICE_URL")


def send_sms(text: str, phone_number: str) -> bool:
    url = f"{_base_url}?login={_username}&psw={_password}&phones={phone_number}&mes={text}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False
