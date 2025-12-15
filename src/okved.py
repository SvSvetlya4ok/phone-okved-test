import json
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass(frozen=True)
class OkvedItem:
    """Элемент справочника ОКВЭД."""
    code: str
    name: str


class OkvedLoadError(RuntimeError):
    """Ошибка загрузки или парсинга ОКВЭД."""


class OkvedLoader:
    """Загружает и разворачивает okved.json по HTTPS."""

    def load(self, url: str) -> List[OkvedItem]:
        """Загружает okved.json и возвращает плоский список ОКВЭД."""

        if not url.startswith("https://"):
            raise OkvedLoadError("URL должен начинаться с https://")

        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise OkvedLoadError("не удалось загрузить okved.json") from exc

        return list(self._flatten(data))

    def _flatten(self, node: Any) -> Iterable[OkvedItem]:
        """Рекурсивно разворачивает дерево ОКВЭД в плоский список."""
        if isinstance(node, dict):
            code = node.get("code")
            name = node.get("name")

            if isinstance(code, str) and isinstance(name, str):
                yield OkvedItem(code=code, name=name)

            items = node.get("items")
            if isinstance(items, list):
                for child in items:
                    yield from self._flatten(child)

        elif isinstance(node, list):
            for item in node:
                yield from self._flatten(item)