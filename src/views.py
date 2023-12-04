import os

from dotenv import load_dotenv

from src.utils import currency_rates, greeting, last_digits, stock_prices

load_dotenv()

FIN_API_KEY = os.getenv("FIN_API_KEY")
EX_R_API_KEY = os.getenv("EX_R_API_KEY")


def generate_json_response(datetime_str: str, cards: list, transactions: list) -> dict:
    """
    Генерирует json-ответ.

    :param datetime_str: Строка с датой и временем.
    :param cards: Список карт.
    :param transactions: Список транзакций.
    :return: Json-ответ.
    """
    currencies = ["USD", "EUR"]

    currency_rates_data = currency_rates(currencies)

    stock_prices_data = stock_prices(FIN_API_KEY)

    json_response = {
        "greeting": greeting(),
        "datetime": datetime_str,
        "cards": [
            {
                "last_digits": last_digits(card["last_digits"]),
                "total_spent": card["total_spent"],
                "cashback": card["total_spent"] // 100,
            }
            for card in cards
        ],
        "top_transactions": [
            {
                "date": transaction["date"],
                "amount": transaction["amount"],
                "category": transaction["category"],
                "description": transaction["description"],
            }
            for transaction in transactions
        ],
        "currency_rates": [{"currency": currency, "rate": rate} for currency, rate in currency_rates_data],
        "stock_prices": [{"stock": stock, "price": price} for stock, price in stock_prices_data.items()],
    }
    return json_response
