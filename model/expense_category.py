import dataclasses
from typing import Optional


@dataclasses.dataclass
class ExpenseCategory:
    user_id: int
    category_name: str
    id: Optional[int] = None
