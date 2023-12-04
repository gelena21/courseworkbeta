import datetime
import logging
import math
import os
from pathlib import Path

from settings import OPERATIONS_PATH
from src.utils import get_data_excel

data_path_log = Path(__file__).parent.parent.joinpath("data", "services.log.")
logger = logging.getLogger("__services__")

if os.path.exists(data_path_log):
    os.remove(data_path_log)

file_handler = logging.FileHandler(data_path_log)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

transactions_dict = get_data_excel(str(OPERATIONS_PATH.resolve())).to_dict(orient="records")


def invest_copilka(month: str, transactions: list[dict], limit: int) -> float:
    """Рассчитывает сумму в копилке путем округления платежей за выбранный срок с выбранным лимитом.

    :param month: Месяц в формате YYYY-MM.
    :param transactions: Список транзакций.
    :param limit: Предел для округления суммы операций.
    :return: Сумма для отложения в инвесткопилку.
    """
    money_in_copilka = 0
    try:
        if limit <= 0:
            raise ValueError("Limit must be a positive value")
        date_obj = datetime.datetime.strptime(month, "%Y-%m")
        corr_month = date_obj.strftime("%m.%Y")
        required_transactions = [
            transaction
            for transaction in transactions
            if transaction["Дата операции"].startswith(corr_month) and transaction["Статус"] == "OK"
        ]
        for transaction in required_transactions:
            if transaction["Сумма платежа"] < 0 and abs(int(transaction["Сумма платежа"])) % limit != 0:
                payment_amount = abs(transaction["Сумма платежа"])
                if limit == 50:
                    rounded_amount = math.ceil(payment_amount / 100) * 100
                    difference = rounded_amount - payment_amount - limit
                    if difference <= 0:
                        round_amount = rounded_amount - payment_amount
                    else:
                        round_amount = difference
                elif limit == 10 or limit == 100:
                    round_amount = math.ceil(payment_amount / limit) * limit - payment_amount
                else:
                    round_amount = 0
                money_in_copilka += round_amount
        logger.info("Копилка успешно наполнена")
        return round(money_in_copilka, 2)
    except (ValueError, KeyError, TypeError) as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции invest_copilka()")
        raise
