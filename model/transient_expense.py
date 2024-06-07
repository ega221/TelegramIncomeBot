import dataclasses
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclasses.dataclass
class TransientExpense:
    telegram_id: Optional[int] = None
    category_name: Optional[str] = None
    value: Optional[Decimal] = None
    date: Optional[datetime] = None
