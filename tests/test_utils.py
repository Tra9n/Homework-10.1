import json

from unittest.mock import mock_open, patch

from src.utils import get_operations, load_operations


def test_load_operations_success() -> None:
    mock_data = [{"id": 1}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("json.load", return_value=mock_data):
            assert load_operations("test.json") == mock_data


def test_load_operations_file_not_found() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert load_operations("test.json") == []


def test_get_operations_rub() -> None:
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    assert get_operations(transaction) == 100.0


def test_get_operations_usd_success() -> None:
    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"rates": {"RUB": 90.5}}

        result = get_operations(transaction)
        assert result == round(10 * 90.5, 2)


def test_get_operations_usd_api_error() -> None:
    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        assert get_operations(transaction) == 0.0


def test_get_operations_invalid_amount() -> None:
    transaction = {"operationAmount": {"amount": "abc", "currency": {"code": "RUB"}}}
    assert get_operations(transaction) == 0.0
