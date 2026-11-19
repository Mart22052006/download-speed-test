from collections.abc import Callable

from messages import INVALID_MEASUREMENT_TIME_MESSAGE
from models import DownloadMeasurement, DownloadSummary


REQUEST_COUNT = 10
Downloader = Callable[[str], DownloadMeasurement]


def measure_downloads(address: str, download: Downloader) -> DownloadSummary:
    total_bytes = 0
    total_seconds = 0.0

    for _ in range(REQUEST_COUNT):
        measurement = download(address)
        total_bytes += measurement.downloaded_bytes
        total_seconds += measurement.elapsed_seconds

    if total_seconds <= 0:
        raise ValueError(INVALID_MEASUREMENT_TIME_MESSAGE)

    average_ms = total_seconds * 1000 / REQUEST_COUNT
    speed_mbps = total_bytes * 8 / total_seconds / 1_000_000
    return DownloadSummary(total_bytes, average_ms, speed_mbps)
