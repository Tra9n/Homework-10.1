from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_namber: str) -> str:
    """Функция которая умеет обрабатывать информацию как о картах, так и о счетах."""
    card_namber = card_namber.strip()

    if not card_namber:
        raise ValueError("Неверный номер карты или счёта")

    last_20 = card_namber[-20:]

    if last_20.isdigit() and len(last_20) == 20:
        prefix = card_namber[:-20].strip()
        if prefix.lower() in ("счет", "счёт"):
            return f"Счет {get_mask_account(last_20)}"
        else:
            raise ValueError("Неверный номер карты или счёта")

    last_16 = card_namber[-16:]

    if last_16.isdigit() and len(last_16) == 16:
        card_name = card_namber[:-16].strip()
        if card_name and len(card_name) > 0:
            return f"{card_name} {get_mask_card_number(last_16)}"
        else:
            raise ValueError("Неверный номер карты или счёта")

    raise ValueError("Неверный номер карты или счёта")


def get_date(time_card: str) -> str:
    """
    Принимает системную дату/время, возвращает
    дату в формате ДД.ММ.ГГГГ
    """
    time_card = time_card.strip()
    if len(time_card) < 10:
        raise IndexError("Строка слишком короткая для извлечения даты")
    return time_card[8:10] + "." + time_card[5:7] + "." + time_card[:4]
