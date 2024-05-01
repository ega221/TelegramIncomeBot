import dataclasses


@dataclasses.dataclass
class IncomeCategory:
    id: int
    user_id: int
    category_name: str
