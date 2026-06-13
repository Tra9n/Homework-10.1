from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from src.operations import get_transactions_from_csv, get_transactions_from_pandas


@pytest.fixture
def sample_csv(tmp_path: Path) -> str:
    csv_file = tmp_path / "transactions.csv"
    csv_content = """id;amount;currency;description
1;100.50;USD;Покупка
2;200.75;RUB;Оплата"""
    csv_file.write_text(csv_content, encoding="utf-8")
    return str(csv_file)


def test_get_transactions_from_csv_success(sample_csv: str, capsys: Any) -> None:
    get_transactions_from_csv(sample_csv)
    captured = capsys.readouterr()

    assert "1" in captured.out
    assert "100.50" in captured.out
    assert "USD" in captured.out
    assert "Покупка" in captured.out


def test_get_transactions_from_csv_file_not_found(capsys: Any) -> None:
    get_transactions_from_csv("not_found.csv")
    captured = capsys.readouterr()

    assert "not_found.csv" in captured.out
    assert "No such file" in captured.out or "не найден" in captured.out


def test_get_transactions_from_csv_empty(tmp_path: Path, capsys: Any) -> None:
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("id;name", encoding="utf-8")

    get_transactions_from_csv(str(empty_file))
    captured = capsys.readouterr()

    assert captured.out == ""


def test_get_transactions_from_csv_returns_none(sample_csv: str) -> None:
    result = get_transactions_from_csv(sample_csv)  # type: ignore
    assert result is None


@pytest.fixture
def sample_excel(tmp_path: Path) -> str:
    excel_file = tmp_path / "transactions_excel.xlsx"
    df = pd.DataFrame({"id": [1, 2, 3], "amount": [100.50, 200.75, 300.00], "currency": ["USD", "RUB", "EUR"]})
    df.to_excel(excel_file, index=False)
    return str(excel_file)


def test_get_transactions_from_pandas_success(sample_excel: str, capsys: Any) -> None:
    get_transactions_from_pandas(sample_excel)
    captured = capsys.readouterr()

    assert "(3, 3)" in captured.out
    assert "100.50" in captured.out
    assert "USD" in captured.out


def test_get_transactions_from_pandas_file_not_found(capsys: Any) -> None:
    get_transactions_from_pandas("not_found.xlsx")
    captured = capsys.readouterr()

    assert "No such file" in captured.out or "not_found.xlsx" in captured.out


def test_get_transactions_from_pandas_returns_none(sample_excel: str) -> None:
    result = get_transactions_from_pandas(sample_excel)  # type: ignore
    assert result is None


def test_get_transactions_from_pandas_empty_file(tmp_path: Path, capsys: Any) -> None:
    empty_file = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_file, index=False)

    get_transactions_from_pandas(str(empty_file))
    captured = capsys.readouterr()

    assert "(0, 0)" in captured.out or "0 rows" in captured.out
