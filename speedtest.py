import sys
from urllib.parse import urlsplit

URL_SCHEME = ["http", "https"]
def main() -> int:
    address = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        url = urlsplit(address)
    except ValueError:
        url = None

    if url is None or url.scheme not in URL_SCHEME or not url.hostname:
        print("Укажите адрес HTTP или HTTPS", file = sys.stderr)
        return 1

print(address)
raise SystemExit(main())