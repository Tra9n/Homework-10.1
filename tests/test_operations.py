from pathlib import Path

import pandas as pd
import pytest

from src.operations import get_transactions_from_csv, get_transactions_from_pandas


@pytest.fixture
def sample_csv(tmp_path: Path) -> str:
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text("id;amount;currency\n1;100.50;USD\n2;200.75;RUB", encoding="utf-8")
    return str(csv_file)


def test_get_transactions_from_csv_success(sample_csv: str) -> None:
    result = get_transactions_from_csv(sample_csv)
    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[0]["amount"] == "100.50"


def test_get_transactions_from_csv_file_not_found() -> None:
    result = get_transactions_from_csv("not_found.csv")
    assert result == []


@pytest.fixture
def sample_excel(tmp_path: Path) -> str:
    excel_file = tmp_path / "transactions.xlsx"
    df = pd.DataFrame({"id": [1, 2], "amount": [100.50, 200.75], "currency": ["USD", "RUB"]})
    df.to_excel(excel_file, index=False)
    return str(excel_file)


def test_get_transactions_from_pandas_success(sample_excel: str) -> None:
    result = get_transactions_from_pandas(sample_excel)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 100.50
    assert result[0]["currency"] == "USD"


def test_get_transactions_from_pandas_file_not_found() -> None:
    result = get_transactions_from_pandas("not_found.xlsx")

    assert result == []
