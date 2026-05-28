from typing import Union

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "num,exp",
    [
        ("7158300734726758", "7158 30** **** 6758"),
        ("7158 3007 3472 6758", "7158 30** **** 6758"),
        (7158300734726758, "7158 30** **** 6758"),
    ],
)
def test_card_valid(num: str, exp: str) -> None:
    assert get_mask_card_number(num) == exp


@pytest.mark.parametrize("num", ["", "12345", "abcd1234efgh5678"])
def test_card_invalid(num: str) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(num)


@pytest.mark.parametrize(
    "num, exp",
    [
        ("73654108430135874305", "**4305"),
        ("7365 4108 4301 3587 4305", "**4305"),
        (73654108430135874305, "**4305"),
    ],
)
def test_account_valid(num: Union[str, int], exp: str) -> None:
    """Тест корректных номеров счетов"""
    assert get_mask_account(num) == exp


@pytest.mark.parametrize(
    "num",
    [
        "",
        "12345",
        "1234567890123456789",
        "123456789012345678901",
        "abcd1234efgh56789012",
        "1234-5678-9012-3456-7890",
        "7365 4108 4301 3587 430",
    ],
)
def test_account_invalid(num: str) -> None:
    """Тест неверных номеров счетов"""
    with pytest.raises(ValueError):
        get_mask_account(num)
