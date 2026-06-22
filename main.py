import os
import re
import sys
from typing import Any, Dict, List

from src.generators import filter_by_currency  # type: ignore
from src.operations import get_transactions_from_csv, get_transactions_from_pandas  # type: ignore
from src.processing import filter_by_state, sort_by_date  # type: ignore
from src.utils import load_operations  # type: ignore
from src.widget import get_date, mask_account_card  # type: ignore

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Функция для фильтрации транзакций по описанию с использованием регулярных выражений.
    """
    if not search or not data:
        return data

    search_pattern = re.escape(search)

    pattern = re.compile(search_pattern, re.IGNORECASE)

    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def count_operations_by_category(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Функция для подсчета количества операций в каждой категории.
    """
    result = {category: 0 for category in categories}

    for transaction in data:
        description = transaction.get("description", "")
        for category in categories:
            if re.search(category, description, re.IGNORECASE):
                result[category] += 1
                break

    return result


def load_transactions_from_source(source_type: str) -> List[Dict[str, Any]]:
    """Загрузка транзакций из выбранного источника."""
    if source_type == "1":
        data = load_operations("data/operations.json")
        if isinstance(data, dict) and "transactions" in data:
            transactions = data["transactions"]
        elif isinstance(data, list):
            transactions = data
        else:
            transactions = []
        print("Для обработки выбран JSON-файл")
        return transactions  # type: ignore
    elif source_type == "2":
        transactions = get_transactions_from_csv("data/transactions.csv")
        print("Для обработки выбран CSV-файл")
        return transactions
    elif source_type == "3":
        transactions = get_transactions_from_pandas("data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл")
        return transactions
    else:
        return []


def filter_by_status(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по статусу."""
    while True:
        status = input("""
Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
- """).upper()
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            filtered = filter_by_state(transactions, state=status)
            print(f"Операции отфильтрованы по статусу {status}")
            return filtered
        else:
            print(f"Статус операции {status} недоступен")


def sort_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортировка транзакций по дате."""
    while True:
        choice = input("Отсортировать по возрастанию или по убыванию? - ").lower()
        if choice == "по возрастанию":
            return sort_by_date(transactions, reverse=False)  # type: ignore
        elif choice == "по убыванию":
            return sort_by_date(transactions, reverse=True)  # type: ignore
        else:
            print("Не корректный ввод, попробуйте снова")


def filter_by_currency_type(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по валюте."""
    choice = input("Выводить только рублевые транзакции? Да/Нет - ").lower()
    if choice == "да":
        return list(filter_by_currency(transactions, "RUB"))
    return transactions


def filter_by_description(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по описанию."""
    choice = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет - ").lower()
    if choice == "да":
        search_term = input("введите фильтр - ")
        return process_bank_search(transactions, search_term)
    return transactions


def display_transaction(transaction: Dict[str, Any]) -> None:
    """Отображение одной транзакции."""
    if "date" in transaction:
        data_transaction = get_date(transaction["date"])
    else:
        data_transaction = "Дата не указана"

    description = transaction.get("description", "")
    print(f"{data_transaction} {description}")

    if "to" in transaction and transaction["to"]:
        card_to = mask_account_card(transaction["to"])
        if "from" in transaction and transaction["from"]:
            card_from = mask_account_card(transaction["from"])
            print(f"{card_from} -> {card_to}")
        else:
            print(card_to)
    else:
        print("Нет информации о получателе")

    amount_str = ""
    currency_str = ""

    if "operationAmount" in transaction:
        op_amount = transaction["operationAmount"]
        if isinstance(op_amount, dict):
            amount_str = op_amount.get("amount", "")
            currency = op_amount.get("currency", {})
            if isinstance(currency, dict):
                currency_str = currency.get("code", "")
            else:
                currency_str = str(currency) if currency else ""

    if not amount_str and "amount" in transaction:
        amount_str = transaction.get("amount", "")
        currency_str = transaction.get("currency_code", transaction.get("currency", ""))

    if amount_str:
        print(f"Сумма: {amount_str} {currency_str}".strip())
    else:
        print("Сумма не указана")

    print()


def display_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Отображение всех транзакций."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(transactions)}")

    for transaction in transactions:
        display_transaction(transaction)


def main() -> None:
    """Главная функция программы."""
    print("Привет!")
    print("Добро пожаловать в программу работы с банковскими транзакциями.")

    user_input = input("""
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
- """)

    transactions_list = load_transactions_from_source(user_input)

    if not transactions_list:
        print("Транзакции отсутствуют или не найдены")
        return

    transactions_list = filter_by_status(transactions_list)

    if not transactions_list:
        print("Транзакции отсутствуют после фильтрации по статусу")
        return

    sort_choice = input("Отсортировать операции по дате? Да/Нет - ").lower()
    if sort_choice == "да":
        transactions_list = sort_transactions(transactions_list)

    transactions_list = filter_by_currency_type(transactions_list)

    transactions_list = filter_by_description(transactions_list)

    display_transactions(transactions_list)
