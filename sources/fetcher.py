from urllib.error import HTTPError

from urllib.request import urlopen
from time import perf_counter
from models import DownloadMeasurement
from messages import (
        INCOMPLETE_RESPONSE_MESSAGE,
)
TIMEOUT = 30

def download_once(address: str) -> DownloadMeasurement:
    started_at = perf_counter()
    downloaded_bytes = 0

    try:
        response = urlopen(address, timeout=TIMEOUT)
    except HTTPError as error:
        error.close()
        raise

    with response:
        while True:
            chunk = response.read(64 * 1024)
            if not chunk:
                break
            downloaded_bytes += len(chunk)

        content_length = response.headers.get("Content-Length")
        if content_length and content_length.isdecimal():
            if downloaded_bytes != int(content_length):
                raise OSError(INCOMPLETE_RESPONSE_MESSAGE)

        return DownloadMeasurement(
            downloaded_bytes=downloaded_bytes,
            elapsed_seconds=perf_counter() - started_at,
        )