import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def load_operations(file_path: str = "data/operations.json") -> dict:
    """Загружает транзакции из JSON-файла"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            operations = json.load(f)
        return operations  # type: ignore
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return []  # type: ignore


def get_operations(transaction: dict) -> float:
    """
    Функция, принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
    тип данных — float.
    Если транзакция была в USD или EUR,
    происходит обращение к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount")
    currency_dict = operation_amount.get("currency", {})
    currency_code = currency_dict.get("code")
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0
    if currency_code == "RUB":
        return amount
    if currency_code in ("USD", "EUR"):
        try:
            url = "https://api.apilayer.com/exchangerates_data/latest"
            headers = {"apikey": API_KEY} if API_KEY else {}
            params = {"base": currency_code, "symbols": "RUB"}

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code != 200:
                return 0.0
            data = response.json()
            rub_rate = data.get("rates", {}).get("RUB")

            if rub_rate is None:
                return 0.0
            return round(amount * rub_rate, 2)  # type: ignore
        except (requests.RequestException, KeyError, ValueError):
            return 0.0

    return 0.0
