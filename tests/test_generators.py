import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency(expected_filter_by_currency: list) -> None:
    test_usd = filter_by_currency(expected_filter_by_currency, "USD")
    assert next(test_usd) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }

    assert next(test_usd) == {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }

    assert next(test_usd) == {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    }

    test_rub = filter_by_currency(expected_filter_by_currency, "RUB")
    assert next(test_rub) == {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    }
    assert next(test_rub) == {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    }


@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        (
            [
                {"description": "Перевод организации"},
                {"description": "Перевод со счета на счет"},
                {"description": "Перевод со счета на счет"},
                {"description": "Перевод с карты на карту"},
            ],
            [
                "Перевод организации",
                "Перевод со счета на счет",
                "Перевод со счета на счет",
                "Перевод с карты на карту",
            ],
        ),
    ],
)
def test_transaction_descriptions(transactions: list, expected_descriptions: list) -> None:
    test_description = transaction_descriptions(transactions)

    for expected in expected_descriptions:
        assert next(test_description) == expected


@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (
            5325437241823135,
            5325621345823135,
            [
                "5325 4372 4182 3135",
                "5325 4372 4182 3136",
                "5325 4372 4182 3137",
                "5325 4372 4182 3138",
                "5325 4372 4182 3139",
            ],
        )
    ],
)
def test_card_number_generator(start: int, end: int, expected_numbers: list) -> None:
    card_number = card_number_generator(start, end)

    for expected in expected_numbers:
        assert next(card_number) == expected
