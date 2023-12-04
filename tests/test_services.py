import logging
import os
from pathlib import Path
import pytest
from main import transactions
from src.services import invest_copilka
from src.utils import get_data_excel


OPERATIONS_PATH_2 = Path(__file__).parent.joinpath("config.json")
OPERATIONS_PATH = Path(__file__).parent.parent.joinpath("data", "operations.xls")

logger = logging.getLogger("__services__")

data_path_log = Path(__file__).parent.parent.joinpath("data", "services.log.")
if os.path.exists(data_path_log):
    file_handler = logger.handlers[0]
    file_handler.close()
    logger.removeHandler(file_handler)
    os.remove(data_path_log)
transactions_dict = get_data_excel(str(OPERATIONS_PATH.resolve().with_name('operations.xls'))).to_dict(orient="records")


def test_invest_copilka_with_invalid_month():
    month = "invalid-month"
    limit = 50

    with pytest.raises(ValueError):
        invest_copilka(month, transactions, limit)


def test_invest_copilka_with_invalid_limit():
    month = "2021-10"
    limit = 0

    with pytest.raises(ValueError):
        invest_copilka(month, transactions, limit)


def test_invest_copilka_with_empty_transactions():
    month = "2021-10"
    limit = 50

    result = invest_copilka(month, [], limit)

    assert result == 0.0


def test_invest_copilka_with_invalid_transaction():
    month = "2021-10"
    limit = 50

    invalid_transaction = {"Дата операции": "2021-10-01", "Статус": "Invalid"}  # Invalid transaction data

    result = invest_copilka(month, [invalid_transaction], limit)

    assert result == 0.0


def test_invest_copilka_with_negative_limit():
    month = "2021-10"
    limit = -50

    with pytest.raises(ValueError):
        invest_copilka(month, transactions, limit)
