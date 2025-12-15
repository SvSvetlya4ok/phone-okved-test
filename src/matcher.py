import re
from typing import Iterable, Tuple

from src.okved import OkvedItem


class OkvedMatchError(RuntimeError):
    """Ошибка подбора ОКВЭД."""


class OkvedMatcher:
    """Подбирает ОКВЭД с максимальным совпадением по окончанию номера."""

    @staticmethod
    def match(
        phone: str,
        okved_items: Iterable[OkvedItem],
    ) -> Tuple[OkvedItem, int]:
        """Находит ОКВЭД с максимальным совпадением по окончанию номера."""
        phone_digits = re.sub(r"\D+", "", phone)

        best_item = None
        best_match_len = -1

        for item in okved_items:
            okved_digits = re.sub(r"\D+", "", item.code)

            match_len = _suffix_match_len(phone_digits, okved_digits)

            if match_len > best_match_len:
                best_item = item
                best_match_len = match_len

        if best_item is None:
            raise OkvedMatchError("список ОКВЭД пуст")

        return best_item, best_match_len


def _suffix_match_len(a: str, b: str) -> int:
    """Возвращает длину совпадения строк по окончанию."""
    length = 0
    while length < len(a) and length < len(b):
        if a[-1 - length] != b[-1 - length]:
            break
        length += 1
    return length
