import dataclasses
from typing import Optional


@dataclasses.dataclass
class IncomeCategory:
    user_id: int
    category_name: str
    id: Optional[int] = None
