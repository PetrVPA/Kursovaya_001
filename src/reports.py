import csv
from dateutil.relativedelta import relativedelta
from multiprocessing.connection import answer_challenge

import pandas as pd
import logging
from datetime import datetime
from typing import Optional

utils_log = logging.getLogger('reports')
file_utils_log = logging.FileHandler(r'..\data\reports.log', encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)

def writen_to_csv(func):
    '''
    декоратор без параметров для записи результатов работы функции в файл
    :param func:
    :return:
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        utils_log.debug(f'Делай ноль - проверка принятого дата фрейма = {result}')
        result = result.to_dict(orient='records')
        utils_log.debug(f'Делай один - проверка словаря = {result}')
        with open(r'..\data\spending_by_category.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Дата платежа', 'Категория', 'Сумма операции']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in result:
                utils_log.debug(f'Делай два - проверка принятого значения = {row}')
                writer.writerow(row)
        utils_log.debug(f'Делай три - получаем данные от функции = {result}')
        answer = func(*args, **kwargs)
        utils_log.debug(f'Делай четыре - возвращаем значение декорируемой функции = {answer}')
        return answer


    return wrapper

# типизация переменных
@writen_to_csv
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    '''
    С 1.012018 по 31.12.2021г.
    :param transactions:
    :param category:
    :param date:
    :return:
    '''
    utils_log.debug(f'Делай ноль - проверка принятого дата фрейма = {transactions}')
    if date is not None:
        date = datetime.strptime(date, '%Y-%m-%d')
        today_day = date.day
        today_month = date.month
        today_year = date.year
        if today_year>2021 or today_year<2018:
            today_year = 2021
        utils_log.debug(f'Делай раз - проверка введенной даты = {today_day}.{today_month}.{today_year}')
        end_day = date - relativedelta(months=3)
        end_month = end_day.month
        end_year = end_day.year
        end_day = end_day.day

    if date is None:
        today = datetime.today()
        today_day = today.day
        today_month = today.month
        today_year = 2021
        utils_log.debug(f'Делай раз - проверка если дату не ввели = {today_day}.{today_month}.{today_year}')
        end_day = today - relativedelta(months=3)
        end_month = end_day.month
        end_year = end_day.year
        end_day = end_day.day


    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], dayfirst=True)
    spred = transactions[(transactions['Дата платежа'] <= pd.to_datetime(f'{today_year}-{today_month}-{today_day}')) &
                         (transactions['Дата платежа'] >= pd.to_datetime(f'{end_year}-{end_month}-{end_day}'))]
    utils_log.debug(f'Делай два - фильтрация дата фрейма по дате = {spred['Дата платежа']}')

    spred = spred[(spred['Категория']==category)]
    utils_log.debug(f'Делай три - полный датафрейм по дате и категории = {category} = {spred}')

    answer_challenge = spred.loc[:, ['Дата платежа', 'Категория','Сумма операции']]
    utils_log.debug(f'Делай четыре - формирование фрейма ответа = {category} = {answer_challenge}')


    return answer_challenge
