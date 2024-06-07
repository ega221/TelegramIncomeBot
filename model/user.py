"""Класс USER"""

import dataclasses
from typing import Optional


@dataclasses.dataclass
class User:
    """Класс USER"""

    telegram_id: int
    id: Optional[int] = None
