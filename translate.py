import json
import logging
import os
import re
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL")
API_DATA = os.getenv("API_DATA")
headers = json.loads(os.getenv("API_HEADERS", "{}"))


def translate(
    sentence: str,
    to_language: str,
    from_language: str = "auto",
) -> list[str] | None:
    sentence = quote(sentence)
    data = (
        f"async=translate,sl:{from_language},tl:{to_language},"
        f"st:{sentence},{API_DATA}"
    )
    try:
        response = requests.post(
            url=API_URL,
            headers=headers,
            data=data,
            timeout=10,
        )
        pattern = re.compile(r'<span id="tw-answ-target-text">(.*?)</span>')
        matches = pattern.findall(response.text)
    except Exception as e:
        logger.error("Translation failed: %s", e)
        return None

    return matches
