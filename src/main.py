import os
import sys
import json

from src.phone import PhoneNormalizer, PhoneNormalizationError
from src.okved import OkvedLoader, OkvedLoadError
from src.matcher import OkvedMatcher, OkvedMatchError


def main() -> None:
    """Точка входа CLI."""
    if len(sys.argv) < 2:
        print("false: не передан текст с номером телефона", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    okved_url = os.getenv("OKVED_URL")

    if not okved_url:
        print("false: не задана переменная окружения OKVED_URL", file=sys.stderr)
        sys.exit(1)

    try:
        phone = PhoneNormalizer().normalize(text)
        okved_items = OkvedLoader().load(okved_url)
        okved, match_len = OkvedMatcher.match(phone, okved_items)
    except (
        PhoneNormalizationError,
        OkvedLoadError,
        OkvedMatchError,
    ) as exc:
        print(f"false: {exc}", file=sys.stderr)
        sys.exit(1)

    result = {
        "normalized_phone": phone,
        "okved": {
            "code": okved.code,
            "name": okved.name,
        },
        "match_len": match_len,
    }

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
