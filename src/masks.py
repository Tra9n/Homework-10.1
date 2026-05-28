from typing import Union


def get_mask_card_number(number_card: Union[str, int]) -> str:
    """Функцию маскировки номера банковской карты"""
    card_number_str = str(number_card).replace(" ", "")
    if not card_number_str.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_number_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:16]}"


def get_mask_account(number_check: Union[str, int]) -> str:
    """Функцию маскировки номера банковского счета"""
    check_number_str = str(number_check).replace(" ", "")
    if not check_number_str.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    if len(check_number_str) != 20:
        raise ValueError("Номер счёта должен содержать 20 цифр")

    return "**" + check_number_str[-4:]
