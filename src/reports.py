import datetime
import logging
import os
import typing
from functools import wraps
from pathlib import Path

import pandas as pd

data_path_log = Path(__file__).parent.parent.joinpath("data", "reports.log")
logger = logging.getLogger("__reports__")

if os.path.exists(data_path_log):
    os.remove(data_path_log)

file_handler = logging.FileHandler(data_path_log)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def report_to_file(*, filename: str = "") -> typing.Any:
    def wrapper(any_func: typing.Callable) -> typing.Callable:
        """
        Декоратор для сохранения результата функции в файл.
        :param filename: Название файла для сохранения. Если не указано, будет использовано автоматическое название.
        :type filename: str, optional
        :return: Результат выполнения функции.
        :rtype: Any
        """

        @wraps(any_func)
        def inner(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            """
            Внутренняя функция декоратора.

            :param args: Позиционные аргументы функции.
            :param kwargs: Именованные аргументы функции.
            :return: Результат функции.
            """
            result = any_func(*args, **kwargs)
            if filename:
                result.to_csv(filename, index=False, encoding="utf-8")
                logger.info("Файл успешно сохранен")
            else:
                date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                data_path = Path(Path(__file__).parent.parent.joinpath("data", "reports", f"{date}_report.csv"))
                data_path.parent.mkdir(exist_ok=True, parents=True)
                result.to_csv(data_path, index=False, encoding="utf-8")
                logger.info("Файл успешно сохранен")

            return result

        return inner

    return wrapper


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: typing.Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает отчет о расходах по указанной категории за определенный период.

    :param transactions: DataFrame с транзакциями.
    :param category: Категория расходов.
    :param date: Дата анализа в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС". Если не указана, используется текущая дата.
    :return: DataFrame с отчетом о расходах по указанной категории за период.
    """
    if date is None:
        current_date = datetime.datetime.now()
    else:
        current_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    first_date = (current_date - datetime.timedelta(days=90)).strftime("%Y.%m.%d")
    last_date = current_date.strftime("%Y.%m.%d")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    df_by_category = transactions.loc[
        (transactions["Статус"] == "OK")
        & (transactions["Дата операции"] >= first_date)
        & (transactions["Дата операции"] <= last_date)
        & (transactions["Категория"] == category)
    ]
    logger.info("Операции выполнена")
    return df_by_category
