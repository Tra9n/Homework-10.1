from typing import Generator, Iterator, Literal


def filter_by_currency(transactions: list, currency: Literal["USD", "RUB"]) -> Iterator:
    """
    Функция возвращает итератор,
    который поочередно выдает транзакции,
    где валюта операции соответствует заданной
    """
    for i in transactions:
        if i.get("operationAmount"):
            code = i["operationAmount"]["currency"]["code"]
        elif i.get("currency_code"):
            code = i.get("currency_code")
        if code == currency:
            yield i


def transaction_descriptions(transactions: list) -> Generator:
    """
    Генератор принимает список словарей с транзакциями и
    возвращает описание каждой операции по очереди.
    """
    for operation in transactions:
        yield operation["description"]


def card_number_generator(start: int, end: int) -> Generator:
    """
    Генератор который выдает номера банковских карт в формате
    XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от
    0000 0000 0000 0001 до 9999 9999 9999 9999.
    """
    for x in range(start, end + 1):
        card_number = f"{x:016d}"
        card_number_str = " ".join([card_number[x : x + 4] for x in range(0, 16, 4)])
        yield card_number_str
