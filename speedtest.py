import sys

from loguru import logger

from cli.reporting import download_and_log, log_summary
from cli.validation import validate_address
from messages import DOWNLOAD_ERROR_MESSAGE
from service.measurement import measure_downloads


def main() -> int:
    address = sys.argv[1] if len(sys.argv) > 1 else ""

    if not validate_address(address):
        return 1

    try:
        summary = measure_downloads(address, download_and_log)
    except (OSError, ValueError) as error:
        logger.error(DOWNLOAD_ERROR_MESSAGE, error)
        return 1

    log_summary(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
