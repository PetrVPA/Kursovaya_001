from src.reports import spending_by_category
from src.utils import data_frame_work
from src.services import beneficial_cashback
from src.views import greet_function

import logging
import os.path

file_path = os.path.join(r'..\data\log_file.log')
log_path = os.path.abspath(file_path)
file_utils_log = logging.FileHandler(log_path, encoding='utf-8')
utils_log = logging.getLogger('main')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


if __name__ == '__main__':
    '''
    Главная функция проекта
    '''
    answer_full = greet_function()
    print('Для определения выгодных категорий объекта введите интересующий год и месяц.')
    year = int(input('Введите год: '))
    month = int(input('Введите месяц: '))
    answer_full['beneficial_cashback'] = (beneficial_cashback(year, month))
    utils_log.debug(f'Делай шесть - контроль работы = {answer_full}')
    print('Для представления трат по категориям за три месяца введите контрольную дату')
    date = input('Введите дату в формате 2019-04-15: ')
    category_spending = input('Введите интересующую категорию: ')
    category_spending = category_spending.lower()
    category_spending = category_spending.title()
    answer_full['spending_by_category'] = (spending_by_category(data_frame_work(), category_spending, date))
    utils_log.debug(f'Делай семь - контроль работы = {answer_full}')
    print(answer_full)
