import json
import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_operations(file_path: str = "data/operations.json") -> dict:
    """Загружает транзакции из JSON-файла"""
    try:
        logger.info(f"Загружаем данные из файла {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            operations = json.load(f)
        return operations  # type: ignore
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as ex:
        logger.error(f"Произошла ошибка: {ex}")
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
        logger.info("Запус программы")
        amount = float(amount_str)
    except (ValueError, TypeError) as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return 0.0
    if currency_code == "RUB":
        logger.info(f"Принимаем транзакцию в {currency_code}")
        return amount
    if currency_code in ("USD", "EUR"):
        logger.info(f"Принимаем транзакцию в {currency_code}")
        try:
            logger.info("Выполняем запрос для конвертации суммы в рубли")
            url = "https://api.apilayer.com/exchangerates_data/live"
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
        except (requests.RequestException, KeyError, ValueError) as ex:
            logger.error(f"Произошла ошибка: {ex}")
            return 0.0

    return 0.0
