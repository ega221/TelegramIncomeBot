import dataclasses
from datetime import datetime
from decimal import Decimal


@dataclasses.dataclass
class Income:
    id: int
    user_id: int
    category_id: int
    category_name: str
    value: Decimal
    date: datetime
