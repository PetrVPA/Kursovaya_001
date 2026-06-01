from src.utils import data_frame_work
import logging

import pandas as pd
from datetime import datetime

utils_log = logging.getLogger('services')
file_utils_log = logging.FileHandler(r'..\data\services.log', encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


def beneficial_cashback(year:str, month:str) -> list(dict):
    year = int(year)
    month = int(month)
    data_frame_funck = data_frame_work()
    utils_log.debug(f'Делай раз - дата фрейм всех транзакций - {data_frame_funck}')
    # выбираем строки дата фрейма по искомому году и месяцу
    data_frame_funck['Дата платежа'] = pd.to_datetime(data_frame_funck['Дата платежа'],format='%d.%m.%Y')
    data_frame_funck = data_frame_funck[(data_frame_funck['Дата платежа'].dt.year == year) & (data_frame_funck['Дата платежа'].dt.month == month)]
    utils_log.debug(f'Делай два - дата фрейм с исследуемым годом и месяцем - {data_frame_funck['Дата платежа']}')
    # удаляем из датафрейма дубликаты в столбе Категория
    #list_categories = data_frame_funck.drop_duplicates(subset=['Категория'], keep=False)
    list_categories = data_frame_funck['Категория'].unique()
    # создаем список категорий
    #list_categories = list_categories.loc['Категория']
    utils_log.debug(f'Делай три - создан список категорий без повторений - {list_categories}')
    list_categories = list(list_categories)
    answer_sum = {}
    for category in list_categories:
        data_filter = data_frame_funck.loc[(data_frame_funck['Категория'] == category)]
        utils_log.debug(f'Делай четыре - получаем транзакции по очередной категории {category} = {data_filter}')
        data_filter['Сумма платежа'] = data_filter['Сумма платежа'].apply(lambda x: abs(x) if x < 0 else x)
        utils_log.debug(f'Делай пять - избавляемся от минуса {category} = {data_filter}')
        money = data_filter['Сумма платежа'].sum()
        utils_log.debug(f'Делай шесть - получаем сумму по категории {category} = {money}')
        money = money * 0.01
        money = f'{money:.2f}'
        money = float(money)
        answer_sum[category] = money
        utils_log.debug(f'Делай семь - добавляем в словарь очередную категорию и расходы по ней {answer_sum}')
    return answer_sum

