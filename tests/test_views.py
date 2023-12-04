import pytest
from src.views import generate_json_response


@pytest.fixture
def sample_data():
    datetime_str = "2023-11-20 14:30:00"
    cards = [
        {"last_digits": "1234", "total_spent": 5000},
        {"last_digits": "5678", "total_spent": 7500},
    ]
    transactions = [
        {
            "date": "21.12.2021",
            "amount": 1198.23,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
        {"date": "20.12.2021", "amount": 421.00, "category": "Различные товары", "description": "Ozon.ru"},
        {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
        {"date": "16.12.2021", "amount": 453.00, "category": "Бонусы", "description": "Кэшбэк за обычные покупки"},
    ]
    return datetime_str, cards, transactions


def test_generate_json_response(sample_data):
    datetime_str, cards, transactions = sample_data
    json_response = generate_json_response(datetime_str, cards, transactions)

    assert isinstance(json_response, dict)

    required_keys = ["greeting", "cards", "top_transactions", "currency_rates", "stock_prices"]
    for key in required_keys:
        assert key in json_response

    assert isinstance(json_response["greeting"], str)
    assert isinstance(json_response["cards"], list)
    assert all(isinstance(card, dict) and set(card.keys()) == {"last_digits", "total_spent", "cashback"} for card in json_response["cards"])
    assert isinstance(json_response["top_transactions"], list)
    assert all(isinstance(transaction, dict) and set(transaction.keys()) == {"date", "amount", "category", "description"} for transaction in json_response["top_transactions"])
    assert isinstance(json_response["currency_rates"], list)
    assert all(isinstance(currency, dict) and set(currency.keys()) == {"currency", "rate"} for currency in json_response["currency_rates"])
    assert isinstance(json_response["stock_prices"], list)
    assert all(isinstance(stock, dict) and set(stock.keys()) == {"stock", "price"} for stock in json_response["stock_prices"])
