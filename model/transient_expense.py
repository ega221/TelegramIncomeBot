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

    def to_string(self):
        return "Категория: {category}\nДата: {date}\nСумма: {value}".format(category=self.category_name, date=self.date,
                                                                            value=self.value)
