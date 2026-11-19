import sys
from urllib.parse import urlsplit
from loguru import logger
from enum import Enum
from http.client import IncompleteRead
from urllib.request import urlopen
from time import perf_counter

#можно было енумчики сделать конечно, но это дорого, так что пускай текстовые константы просто будут в массивах
#TODO: добавить отдельный файл с текстовыми константами, разбить скрипт на модули. 
"""
class url_scheme(Enum):
    HTTP = "http"
    HTTPS = "https"

url_scheme = url_scheme()
"""
URL_SCHEME = ("http", "https")
TIMEOUT = 30

def main() -> int:
    address = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        url = urlsplit(address)
    except ValueError:
        url = None

    if url is None:
        logger.error("Не удалось разобрать URL.")
        return 1

    if url.scheme not in URL_SCHEME:
        logger.error("Допустимы только схемы HTTP и HTTPS.")
        return 1

    if not url.hostname:
        logger.error("В URL отсутствует имя хоста.")
        return 1

    try:
        for _ in range(10):
            downloaded_bytes, elapsed_seconds = download_once(address)
            logger.info("Скачано {} байт за {:.3f} с", downloaded_bytes, elapsed_seconds)
    except (OSError, IncompleteRead) as error:
        logger.error("Ошибка скачивания — {}", error)
        return 1

def download_once(address: str) -> tuple[int, float]:
    started_at = perf_counter()
    downloaded_bytes = 0

    with urlopen(address, timeout=TIMEOUT) as response:
        while True:
            chunk = response.read(64 * 1024)
            if not chunk:
                break
            downloaded_bytes += len(chunk)

        content_length = response.headers.get("Content-Length")
        if content_length and content_length.isdecimal():
            if downloaded_bytes != int(content_length):
                raise OSError("Ответ получен не полностью.")

        return downloaded_bytes, perf_counter() - started_at

raise SystemExit(main())
