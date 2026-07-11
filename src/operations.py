import csv
from typing import Any, Dict, List

import pandas as pd


def get_transactions_from_csv(transactions_file: str = "data/transactions.csv") -> List[Dict[str, Any]]:
    """Функция для считывания финансовых операций из Csv"""
    try:
        with open(transactions_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            return list(reader)
    except FileNotFoundError as e:
        print(e)
        return []


def get_transactions_from_pandas(transactions_excel: str = "data/transactions.xlsx") -> List[Dict]:
    """Функция для считывания финансовых операций из Excel"""
    try:
        df = pd.read_excel(transactions_excel)
        return df.to_dict(orient="records")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        return []
