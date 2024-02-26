from utils.SimpleCalculator import add


def test_adding_two_numbers():
    assert add(1, 2) == 3


def test_adding_another_two_numbers():
    assert add(2, 3) == 5


def test_adding_more_numbers():
    assert add(5, 7) == 12
