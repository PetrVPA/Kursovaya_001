from src.reports import spending_by_category
from src.utils import top_trans
from src.utils import data_frame_work
from src.utils import cards_ful_answer
from src.utils import creat_list_cards
from src.utils import greeting_time
from src.utils import choice_parer
from src.services import beneficial_cashback
from src.views import list_paper

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
    answer_full = []
    top_answ_valut = {}
    top_answ_stok = {}
    top_answ_trans = {}
    answer_full.append(greeting_time())
    utils_log.debug(f'Делай ноль - контроль работы = {answer_full}')
    answer_full.append(cards_ful_answer(data_frame_work(), creat_list_cards(data_frame_work())))
    utils_log.debug(f'Делай два - контроль работы = {answer_full}')
    got = top_trans(data_frame_work())
    top_answ_trans['top_transactions'] = got
    answer_full.append(top_answ_trans)
    utils_log.debug(f'Делай три - контроль работы = {answer_full}')
    list_valute = list_paper('valut')
    answer_valut = choice_parer('valut', list_valute)
    answer_full.append(answer_valut)
    list_stok = list_paper('stock')
    answer_stok = choice_parer('stock', list_stok)
    answer_full.append(answer_stok)
    utils_log.debug(f'Делай пять - контроль работы = {answer_full}')
    print('Для определения выгодных категорий объекта введите интересующий год и месяц.')
    year = int(input('Введите год: '))
    month = int(input('Введите месяц: '))
    answer_full.append(beneficial_cashback(year, month))
    utils_log.debug(f'Делай шесть - контроль работы = {answer_full}')
    print('Для представления трат по категориям за три месяца введите контрольную дату')
    date = input('Введите дату в формате 2019-04-15: ')
    category_spending = input('Введите интересующую категорию: ')
    category_spending = category_spending.lower()
    category_spending = category_spending.title()
    answer_full.append(spending_by_category(data_frame_work(), category_spending, date))
    utils_log.debug(f'Делай семь - контроль работы = {answer_full}')
    print(answer_full)
