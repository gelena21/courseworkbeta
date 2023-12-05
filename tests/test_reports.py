import pytest
import pandas as pd
from src.reports import spending_by_category
import logging


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Дата операции': ['2023-09-01 12:34:45', '2023-09-02 12:34:45', '2023-09-05 12:34:45', '2023-10-01 12:34:45', '2023-11-01 12:34:45'],
        'Категория': ['Food', 'Clothing', 'Food', 'Clothing', 'Food'],
        'Статус': ["OK", "OK", "OK", "OK", "OK"]
    })


def test_spending_by_category_default_filename(tmp_path, caplog, sample_data):
    caplog.set_level(logging.INFO)
    assert "Операции выполнена" in caplog.text
    assert "Файл успешно сохранен" in caplog.text


def test_spending_by_category_custom_filename(tmp_path, caplog, sample_data):
    caplog.set_level(logging.INFO)
    assert "Операции выполнена" in caplog.text
    assert "Файл успешно сохранен" in caplog.text
