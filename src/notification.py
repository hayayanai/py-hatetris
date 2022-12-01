from os import getenv
import json

import requests
from dotenv import load_dotenv
load_dotenv(override=True)

webhook_url = getenv("WEBHOOK_URL")


def send_webhook(payload: dict[str: str]) -> int:
    if webhook_url is None:
        print("webhook_url is None")
        exit()

    res = requests.post(webhook_url, {"payload_json": json.dumps(payload)})
    return res.status_code
