import sys
from collections.abc import Callable
from dataclasses import dataclass
from urllib.parse import urlsplit
from loguru import logger
from enum import Enum
from http.client import IncompleteRead
from urllib.error import HTTPError
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
REQUEST_COUNT = 10

@dataclass(frozen=True)
class DownloadMeasurement:
    downloaded_bytes: int
    elapsed_seconds: float

Downloader = Callable[[str], DownloadMeasurement]


@dataclass(frozen=True)
class DownloadSummary:
    total_bytes: int
    average_ms: float
    speed_mbps: float


def main() -> int:
    address = sys.argv[1] if len(sys.argv) > 1 else ""

    if not validate_address(address):
        return 1
    try:
        summary = measure_downloads(address, download_and_log)
    except (OSError, IncompleteRead, ValueError) as error:
        logger.error("Ошибка скачивания — {}", error)
        return 1

    log_summary(summary)
    return 0


def log_summary(summary: DownloadSummary) -> None:
    logger.info("Общий объём — {} байт", summary.total_bytes)
    logger.info("Среднее время запроса — {:.2f} мс", summary.average_ms)
    logger.info("Скорость скачивания — {:.2f} Мбит/с", summary.speed_mbps)

def validate_address(address: str) -> bool:
    try:
        url = urlsplit(address)
    except ValueError:
        url = None
    
    if url is None:
        logger.error("Не удалось разобрать URL.")
        return False
    
    if url.scheme not in URL_SCHEME:
        logger.error("Допустимы только схемы HTTP и HTTPS.")
        return False

    if not url.hostname:
        logger.error("В URL отсутствует имя хоста.")
        return False
    
    return True
    
def measure_downloads(address: str, download: Downloader) -> DownloadSummary:
    total_bytes = 0
    total_seconds = 0.0

    for _ in range(REQUEST_COUNT):
        measurement = download(address)
        total_bytes += measurement.downloaded_bytes
        total_seconds += measurement.elapsed_seconds

    if total_seconds <= 0:
        raise ValueError("Суммарное время замера должно быть положительным.")

    average_ms = total_seconds * 1000 / REQUEST_COUNT
    speed_mbps = total_bytes * 8 / total_seconds / 1_000_000
    return DownloadSummary(total_bytes, average_ms, speed_mbps)

def download_and_log(address: str) -> DownloadMeasurement:
    measurement = download_once(address)
    logger.info(
        "Скачано {} байт за {:.3f} с",
        measurement.downloaded_bytes,
        measurement.elapsed_seconds,
    )
    return measurement


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
                raise OSError("Ответ получен не полностью.")

        return DownloadMeasurement(
            downloaded_bytes=downloaded_bytes,
            elapsed_seconds=perf_counter() - started_at,
        )

if __name__ == "__main__":
    raise SystemExit(main())
