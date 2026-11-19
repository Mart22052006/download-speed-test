from dataclasses import dataclass


@dataclass(frozen=True)
class DownloadMeasurement:
    downloaded_bytes: int
    elapsed_seconds: float

@dataclass(frozen=True)
class DownloadSummary:
    total_bytes: int
    average_ms: float
    speed_mbps: float