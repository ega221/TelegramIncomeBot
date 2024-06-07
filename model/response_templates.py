"""Файл с Pydantic классами для Update из Tg"""

from dataclasses import dataclass


@dataclass
class Update:
    """Класс, соответствующий tg update"""

    telegram_id: int
    text: str
    update_id: int
