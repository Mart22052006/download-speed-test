import sys
from urllib.parse import urlsplit
from enum import Enum
from http.client import IncompleteRead
from urllib.request import urlopen
from time import perf_counter

#можно было енумчик сделать конечно, но это дорого, так что пускай текстовые константы просто будут в кортеже
"""
class url_scheme(Enum):
    HTTP = "http"
    HTTPS = "https"

url_scheme = url_scheme()
"""
URL_SCHEME = ("http", "https")

def main() -> int:
    address = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        url = urlsplit(address)
    except ValueError:
        url = None

    if url is None or url.scheme not in URL_SCHEME or not url.hostname:
        print("Укажите адрес HTTP или HTTPS", file = sys.stderr)
        return 1
    
    try:
        for _ in range(10):
            downloaded_bytes, elapsed_seconds = download_once(address)
            print(f"Скачано {downloaded_bytes} байт за {elapsed_seconds:.3f} с")
    except (OSError, IncompleteRead) as error:
        print("Ошибка скачивания!")
        return 1

def download_once(address: str) -> tuple[int, float]:
    started_at = perf_counter()

    with urlopen(address, timeout=30) as response:
        downloaded_bytes = len(response.read())
        return downloaded_bytes, perf_counter() - started_at

raise SystemExit(main())