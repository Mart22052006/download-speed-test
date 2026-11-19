from urllib.parse import urlsplit

from loguru import logger

from messages import INVALID_URL_MESSAGE, MISSING_HOST_MESSAGE, UNSUPPORTED_SCHEME_MESSAGE


URL_SCHEME = ("http", "https")


def validate_address(address: str) -> bool:
    try:
        url = urlsplit(address)
    except ValueError:
        url = None

    if url is None:
        logger.error(INVALID_URL_MESSAGE)
        return False

    if url.scheme not in URL_SCHEME:
        logger.error(UNSUPPORTED_SCHEME_MESSAGE)
        return False

    if not url.hostname:
        logger.error(MISSING_HOST_MESSAGE)
        return False

    return True
