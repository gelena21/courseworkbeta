import json
from settings import OPERATIONS_PATH, OPERATIONS_PATH_2
from src.utils import greeting, last_digits, get_data_excel
from src.views import generate_json_response
from src.services import invest_copilka, transactions_dict

with open(OPERATIONS_PATH_2, "r") as config_file:
    config_data = json.load(config_file)
    user_currencies = config_data.get("user_currencies", [])
    user_stocks = config_data.get("user_stocks", [])


transactions = get_data_excel(OPERATIONS_PATH).to_dict(orient="records")

greeting_message = greeting()
total_spent_data = [{"last_digits": last_digits(card), "total_spent": 1000} for card in ["1234567890123456", "9876543210987654"]]
cashback_value = 10.5
top_transactions_data = [
    {"date": "01.01.2023", "amount": 500, "category": "Groceries", "description": "Grocery shopping"},
    {"date": "02.01.2023", "amount": 200, "category": "Clothing", "description": "Clothes shopping"}
]
currency_rates_data = [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 90.0}]  # Замените реальными данными
stock_prices_data = {"AAPL": 150.0, "AMZN": 3000.0}

month = "2023-01"
limit = 50
invested_amount = invest_copilka(month, transactions_dict, limit)

json_response = generate_json_response(
    datetime_str="2023-01-01",
    cards=total_spent_data,
    transactions=top_transactions_data
)

print("Greeting:", greeting_message)
print("Invested amount:", invested_amount)
print("JSON Response:", json_response)
