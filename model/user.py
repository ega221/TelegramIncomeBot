import dataclasses
from typing import Optional


@dataclasses.dataclass
class User:
    telegram_id: int
    id: Optional[int] = None
