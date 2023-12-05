import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

from settings import OPERATIONS_PATH

data_path_log = Path(__file__).parent.parent.joinpath("data", "utils.log")
logger = logging.getLogger("__utils__")

if os.path.exists(data_path_log):
    os.remove(data_path_log)

file_handler = logging.FileHandler(data_path_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def get_data_excel(filename: str) -> pd.DataFrame:
    """Загружает данные из excel файла"""

    return pd.read_excel(filename, engine="xlrd")


def get_data_for_analysis(transactions: pd.DataFrame, data: str = "") -> pd.DataFrame:
    """
    Фильтрует операции для анализа по временным границам.

    :param transactions: Датафрейм с транзакциями.
    :return: Отфильтрованный датафрейм для анализа.
    """
    if data == "":
        date_obj = datetime.now().date()
    else:
        date_obj = datetime.strptime(data, "%d.%m.%Y")

    start_date = date_obj.strftime("%Y.%m.01")
    end_date = date_obj.strftime("%Y.%m.%d")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    modif_df = transactions.loc[
        (transactions["Статус"] == "OK")
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]
    return modif_df


def greeting() -> str:
    """
    Возвращает приветствие в зависимости от текущего времени.

    :return: Приветствие.
    """
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting_message = "Доброе утро"
    elif 12 <= current_hour < 18:
        greeting_message = "Добрый день"
    elif 18 <= current_hour < 23:
        greeting_message = "Добрый вечер"
    else:
        greeting_message = "Доброй ночи"

    logger.info(f"Приветствие:{greeting_message}")
    return greeting_message


def last_digits(card_number: str) -> str:
    """
    Возвращает последние 4 цифры номера карты.

    :param card_number: Номер карты.
    :return: Последние 4 цифры карты.
    """
    return card_number[-4:]


def total_spent(cards: list) -> list[dict]:
    """
    Возвращает сумму расходов по каждой карте.

    :param cards: Список карт.
    :return: Список словарей с суммой расходов по каждой карте.
    """
    return [{"last_digits": last_digits(card["Номер карты"]), "total_spent": card["Сумма операции"]} for card in cards]


def cashback(cards: List[Dict[str, float]]) -> float:
    """
    Возвращает общую сумму кэшбэка по картам.

    :param cards: Список карт.
    :return: Общая сумма кэшбэка.
    """
    return sum(card["Сумма операции"] * 0.01 for card in cards)


def top_transactions(transactions_df: pd.DataFrame) -> List[Dict[str, Union[str, int, None]]]:
    """
    Возвращает топ-5 транзакций по сумме платежа.

    :param transactions_df: Объект pandas DataFrame с транзакциями.
    :return: Топ-5 транзакций.
    """
    df = transactions_df.loc[(transactions_df["Сумма операции"] < 0) & (transactions_df["Валюта операции"] == "RUB")]
    new_df = df.loc[df["Номер карты"] != ""]

    top_transactions_5 = new_df.sort_values(by=["Сумма операции"], ascending=True).head(5).to_dict(orient="records")
    result_list = []

    for i in top_transactions_5:
        result_dict = dict.fromkeys(["date", "amount", "category", "description"], None)
        result_dict["date"] = pd.Timestamp(i["Дата операции"]).strftime("%d.%m.%Y") if "Дата операции" in i else None
        result_dict["amount"] = abs(i["Сумма операции"])
        result_dict["category"] = i.get("Категория")
        result_dict["description"] = i.get("Описание")

        result_list.append(result_dict)

    logger.info("Данные успешно преобразованы")
    return result_list


def currency_rates(currencies: List[str]) -> list[dict]:
    """
    Получает курсы валют за указанный временной период.

    :param api_key:
    :param currencies: Список валют.
    :param first_date_obj: Начальная дата временного периода.
    :param last_date_obj: Конечная дата временного периода.
    :return: Список словарей с курсами валют за указанный период.
    """
    load_dotenv()
    api_key = os.getenv("EX_R_API_KEY")
    if api_key is None:
        logging.error("API ключ отсутствует")
        raise ValueError("API ключ отсутствует")

    url = "https://api.apilayer.com/exchangerates_data/latest?base=RUB"
    headers = {"apikey": api_key}
    currency_rates = []

    response = requests.request("GET", url, headers=headers, data=[])
    response.raise_for_status()
    data = response.json()

    for currency in currencies:
        if currency in data.get("rates", {}):
            rate_data = {"currency": currency, "exchange_rate": round(1 / data["rates"][currency], 2)}
            currency_rates.append(rate_data)

    return currency_rates


def stock_prices(key) -> dict[str, Any]:
    """
    Возвращает цены на акции из S&P 500.

    :param key:
    :return: Словарь с ценами на акции.
    """
    load_dotenv()
    api_key = os.getenv("FIN_API_KEY")
    if api_key is None:
        logging.error("API ключ отсутсвует")
        raise ValueError("API ключ отсутсвует")

    stock_prices_data = {}
    for stock in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}"
        response = requests.get(url)
        data = response.json()
        stock_price = data["c"]
        stock_prices_data[stock] = stock_price

    return stock_prices_data


def make_transactions(transactions: pd.DataFrame) -> DataFrame | DataFrame:
    transactions = get_data_excel(str(OPERATIONS_PATH))
    return transactions
