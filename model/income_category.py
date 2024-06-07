"""IncomeCategory"""

import dataclasses
from typing import Optional


@dataclasses.dataclass
class IncomeCategory:
    """IncomeCategory"""

    user_id: int
    category_name: str
    id: Optional[int] = None
