import csv

import pandas as pd


def get_transactions_from_csv(transactions_file: str = "data/transactions.csv") -> None:
    """Функция для считывания финансовых операций из Csv"""
    try:
        with open(transactions_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                print(row)

    except FileNotFoundError as e:
        print(e)


def get_transactions_from_pandas(transactions_excel: str = "data/transactions_excel.xlsx") -> None:
    """Функция для считывания финансовых операций из Excel"""
    try:
        df = pd.read_excel(transactions_excel)
        print(df.shape)
        print(df.head())

    except FileNotFoundError as e:
        print(e)
