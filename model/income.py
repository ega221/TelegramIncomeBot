"""Income"""

import dataclasses
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclasses.dataclass
class Income:
    """Income"""

    user_id: int
    category_id: int
    value: Decimal
    date: datetime
    id: Optional[int] = None
