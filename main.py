import os
import sys

from src.generators import filter_by_currency  # type: ignore
from src.operations import get_transactions_from_csv, get_transactions_from_pandas  # type: ignore
from src.processing import filter_by_state, sort_by_date  # type: ignore
from src.utils import load_operations, process_bank_search  # type: ignore
from src.widget import mask_account_card  # type: ignore

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def main() -> None:
    user_input = input("""Привет!
Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
- """)
    transactions_list = []  # type: ignore
    while True:
        if user_input == "1":
            transactions_list = load_operations("data/operations.json")  # type: ignore
            print("Для обработки выбран JSON-файл")
            break
        elif user_input == "2":
            transactions_list = get_transactions_from_csv("data/transactions.csv")
            print("Для обработки выбран CSV-файл")
            break
        elif user_input == "3":
            transactions_list = get_transactions_from_pandas("data/transactions_excel.xlsx")
            print("Для обработки выбран XLSX-файл")
            break
        else:
            user_input = input("не верный ввод, повторите")
    while True:
        user_input = input("""
Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
- """).upper()
        if user_input in ["EXECUTED", "CANCELED", "PENDING"]:

            transactions_list = filter_by_state(transactions_list, state=user_input)
            print(f"Операции отфильтрованы по статусу {user_input}")
            break
        else:
            print(f"Статус операции {user_input} недоступен")
    if transactions_list == ([], "Данные не найдены"):
        print("Транзакции отсутствуют")
        exit()
    user_input = input("Отсортировать операции по дате? Да/Нет - ").lower()

    if user_input == "да":
        while True:
            user_input = input("Отсортировать по возрастанию или по убыванию? - ").lower()
            if user_input == "по возрастанию":
                sorting = False
            elif user_input == "по убыванию":
                sorting = True
            else:
                print("не корректный ввод, попробуйте снова")
                continue
            transactions_list = sort_by_date(transactions_list, reverse=sorting)
            break

    user_input = input("Выводить только рублевые транзакции? Да/Нет - ").lower()

    if user_input == "да":
        transactions_list = list(filter_by_currency(transactions_list, "RUB"))

    user_input = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет - ").lower()
    if user_input == "да":
        user_input = input("введите фильтр - ")
        transactions_list = process_bank_search(transactions_list, user_input)

    len_transaktion = len(transactions_list)
    if len_transaktion == 0:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print("Распечатываю итоговый список транзакций")
        print(f"Всего банковских операций в выборке: {len_transaktion}")
        for transaction in transactions_list:
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
