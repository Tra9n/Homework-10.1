import pytest

from src.widget import get_date, mask_account_card

# Тест для mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ],
)
def test_mask_account_card(value: str, expected: str) -> None:
    """Тест корректной маскировки карт и счетов"""
    assert mask_account_card(value) == expected


@pytest.mark.parametrize(
    "value, expected_message",
    [
        ("Счёт 12345", "Неверный номер карты или счёта"),
        ("Some text", "Неверный номер карты или счёта"),
        ("", "Неверный номер карты или счёта"),
        ("Maestro 159683786870519954353424235", "Неверный номер карты или счёта"),
    ],
)
def test_mask_account_card_invalid(value: str, expected_message: str) -> None:
    """Проверяем, что функция выбрасывает ValueError"""
    with pytest.raises(ValueError, match=expected_message):
        mask_account_card(value)


# Тесты для get_date


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2024/03/11T02:26:18", "11.03.2024"),
        ("2024-03-11T02:26:18", "11.03.2024"),
    ],
)
def test_get_date_valid(input_date: str, expected: str) -> None:
    """Тест корректного преобразования даты"""
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "",
        "2024-03",
        "no date",
        "T02:26",
    ],
)
def test_get_date_invalid(invalid_date: str) -> None:
    """Тест: функция выбрасывает IndexError при неверных данных"""
    with pytest.raises(IndexError):
        get_date(invalid_date)
