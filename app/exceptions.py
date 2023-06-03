from typing import Dict


class ExceptionDescribed(Exception):
    code: str = "GE-0001"
    status_code: int = 500
    description: Dict[str, str] = {
        "ru": "Неизвестная ошибка",
        "en": "Unknown error"
    }
