import re

class PhoneNormalizationError(ValueError):
    """Ошибка нормализации номера телефона."""

class PhoneNormalizer:
    """Приводит российский мобильный номер к формату +79XXXXXXXXX."""

    _NON_DIGITS = re.compile(r"\D+")

    def normalize(self, text: str) -> str:
        """Нормализует номер телефона из произвольного текста."""
        digits = self._NON_DIGITS.sub("", text)

        if len(digits) == 10:
            digits = "7" + digits

        if len(digits) == 11 and digits.startswith("8"):
            digits = "7" + digits[1:]

        if len(digits) != 11:
            raise PhoneNormalizationError("номер должен содержать 10 или 11 цифр")

        if not digits.startswith("7"):
            raise PhoneNormalizationError("код страны должен быть 7")

        if digits[1] != "9":
            raise PhoneNormalizationError("номер не является мобильным")

        return "+" + digits