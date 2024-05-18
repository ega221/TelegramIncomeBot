import dataclasses


@dataclasses.dataclass
class ExpenseCategory:
    id: int
    user_id: int
    category_name: str
