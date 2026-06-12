import logging
from typing import Union

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number_card: Union[str, int]) -> str:
    """Функцию маскировки номера банковской карты"""
    card_number_str = str(number_card).replace(" ", "")
    logger.info(f"Вызвана get_mask_card_number с номером {card_number_str}")

    if not card_number_str.isdigit():
        logger.error(f"Номер карты {card_number_str} должен содержать только цифры")
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_number_str) != 16:
        logger.error(f"Номер карты имеет {len(card_number_str)} цифр, должен содержать 16 цифр")
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:16]}"


def get_mask_account(number_check: Union[str, int]) -> str:
    """Функцию маскировки номера банковского счета"""
    check_number_str = str(number_check).replace(" ", "")
    logger.info(f"Вызвана get_mask_account с номером счёта {check_number_str}")
    if not check_number_str.isdigit():
        logger.error(f"Номер счёта {check_number_str} должен содержать только цифры")
        raise ValueError("Номер счёта должен содержать только цифры")

    if len(check_number_str) != 20:
        logger.error(f"Номер карты счёта {len(check_number_str)} цифр, должен содержать 20 цифр")
        raise ValueError("Номер счёта должен содержать 20 цифр")

    return "**" + check_number_str[-4:]
