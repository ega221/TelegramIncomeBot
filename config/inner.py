"""Класс - состояние для машины состояний"""


class Inner:
    """Класс - состояние для машины состояний"""

    def __init__(self, value, nxt, func):
        self.value = value
        self.nxt = nxt
        self.func = func
