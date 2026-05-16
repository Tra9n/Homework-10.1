import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_executed(library: list, expected_executed: list) -> None:
    """Тест фильтрации по статусу EXECUTED"""
    assert filter_by_state(library, "EXECUTED") == expected_executed


def test_filter_by_state_canceled(library: list, expected_canceled: list) -> None:
    """Тест фильтрации по статусу CANCELED"""
    assert filter_by_state(library, "CANCELED") == expected_canceled


def test_filter_by_state_no_matches(library: list) -> None:
    """Тест когда нет элементов с указанным статусом"""
    assert filter_by_state(library, "UNKNOWN") == []


def test_filter_by_state_empty_list() -> None:
    """Тест с пустым списком"""
    assert filter_by_state([], "EXECUTED") == []


@pytest.mark.parametrize(
    "list_dir, descending, expected",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 41428830, "state": "EXECUTED", "date": "2018-06-30T12:45:00.123456"},
                {"id": 41428831, "state": "EXECUTED", "date": "2019-08-01T10:00:00.000000"},
            ],
            True,
            [
                {"id": 41428831, "state": "EXECUTED", "date": "2019-08-01T10:00:00.000000"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 41428830, "state": "EXECUTED", "date": "2018-06-30T12:45:00.123456"},
            ],
        ),
        # Сортировка по возрастанию
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 41428830, "state": "EXECUTED", "date": "2018-06-30T12:45:00.123456"},
                {"id": 41428831, "state": "EXECUTED", "date": "2019-08-01T10:00:00.000000"},
            ],
            False,
            [
                {"id": 41428830, "state": "EXECUTED", "date": "2018-06-30T12:45:00.123456"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 41428831, "state": "EXECUTED", "date": "2019-08-01T10:00:00.000000"},
            ],
        ),
        (
            [
                {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 3, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
            True,
            [
                {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 3, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
        ([], True, []),
        (
            [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}],
            True,
            [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}],
        ),
    ],
)
def test_sort_by_date(list_dir: list, descending: bool, expected: str) -> None:
    assert sort_by_date(list_dir, descending) == expected
