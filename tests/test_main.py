import json
from src.utils import greeting
from src.views import generate_json_response
from src.services import invest_copilka, transactions_dict
import pytest
from settings import OPERATIONS_PATH, OPERATIONS_PATH_2


with open(OPERATIONS_PATH_2, "r") as config_file:
    config_data = json.load(config_file)
    user_currencies = config_data.get("user_currencies", [])
    user_stocks = config_data.get("user_stocks", [])


@pytest.fixture
def sample_excel_file_path():
    return OPERATIONS_PATH


def test_greeting(capfd):
    greeting_message = greeting()
    print("Greeting:", greeting_message)
    captured = capfd.readouterr()
    assert greeting_message in captured.out


def test_invest_copilka(capfd):
    month = "2023-01"
    limit = 50
    invested_amount = invest_copilka(month, transactions_dict, limit)
    print("Invested amount:", invested_amount)
    captured = capfd.readouterr()
    assert "Invested amount:" in captured.out


def test_generate_json_response(capfd):
    datetime_str = "2023-01-01"
    total_spent_data = [{"last_digits": "1234", "total_spent": 100}]
    top_transactions_data = [{"date": "01.01.2023", "amount": 500, "category": "Groceries", "description": "Grocery shopping"}]
    json_response = generate_json_response(datetime_str=datetime_str, cards=total_spent_data, transactions=top_transactions_data)
    print("JSON Response:", json_response)
    captured = capfd.readouterr()
    assert "JSON Response:" in captured.out
