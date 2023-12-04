from src.utils import (
    greeting, last_digits, total_spent, cashback, top_transactions,
    currency_rates, stock_prices, get_data_excel, get_data_for_analysis
)
import pandas as pd
from settings import OPERATIONS_PATH
from src.views import EX_R_API_KEY


def test_get_data_excel():
    result = get_data_excel(OPERATIONS_PATH)
    assert result is not None


def test_get_data_for_analysis():
    transactions = get_data_excel(OPERATIONS_PATH)

    if isinstance(transactions, pd.DataFrame):
        result = get_data_for_analysis(transactions)
        assert result is not None
    else:
        assert transactions == 'Файл с операциями отсутствует'


def test_greeting():
    result = greeting()
    assert isinstance(result, str)


def test_last_digits():
    card_number = "1234567890123456"
    result = last_digits(card_number)
    assert result == "3456"


def test_total_spent():
    cards = [
        {'Номер карты': '1234', 'Сумма операции': 100},
        {'Номер карты': '5678', 'Сумма операции': 200},
        {'Номер карты': '9012', 'Сумма операции': 300},
    ]
    result = total_spent(cards)
    assert result == [
        {"last_digits": "1234", "total_spent": 100},
        {"last_digits": "5678", "total_spent": 200},
        {"last_digits": "9012", "total_spent": 300},
    ]


def test_cashback():
    cards = [
        {'Сумма операции': 100},
        {'Сумма операции': 200},
        {'Сумма операции': 300},
    ]
    result = cashback(cards)
    assert result == 6  # 600 // 100 = 6


def test_top_transactions():
    transactions = get_data_excel(OPERATIONS_PATH)
    result = top_transactions(transactions)

    assert len(result) == 5, f"Expected 5 transactions, but got {len(result)}"


def test_currency_rates():
    result = currency_rates(['USD', 'EUR'])
    assert isinstance(result, list)
    assert all(isinstance(rate, dict) for rate in result)


def test_stock_prices():
    result = stock_prices(EX_R_API_KEY)
    assert isinstance(result, dict)
    if result:
        assert all(stock in result for stock in ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA'])
