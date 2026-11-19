from loguru import logger

from messages import (
    AVERAGE_TIME_MESSAGE,
    DOWNLOAD_PROGRESS_MESSAGE,
    DOWNLOAD_SPEED_MESSAGE,
    TOTAL_BYTES_MESSAGE,
)
from models import DownloadMeasurement, DownloadSummary
from sources.fetcher import download_once


def download_and_log(address: str) -> DownloadMeasurement:
    measurement = download_once(address)
    logger.info(
        DOWNLOAD_PROGRESS_MESSAGE,
        measurement.downloaded_bytes,
        measurement.elapsed_seconds,
    )
    return measurement


def log_summary(summary: DownloadSummary) -> None:
    logger.info(TOTAL_BYTES_MESSAGE, summary.total_bytes)
    logger.info(AVERAGE_TIME_MESSAGE, summary.average_ms)
    logger.info(DOWNLOAD_SPEED_MESSAGE, summary.speed_mbps)
