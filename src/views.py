import logging
import json
import os.path
from src.utils import greeting_time
from src.utils import cards_ful_answer
from src.utils import data_frame_work
from src.utils import top_trans
from src.utils import choice_parer
from src.utils import creat_list_cards


file_path = os.path.join(r'..\data\views.log')
log_path = os.path.abspath(file_path)
utils_log = logging.getLogger('views')
file_utils_log = logging.FileHandler(log_path, encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


def list_paper(type: str) -> list:
    '''
    функция принимает строковое значение выбора валюты 'valut' или акции 'stock' и выдает список либо валют либо акций
    из файла настройки пользователя data/user_settings.json где содержится эта информация.
    :param type:
    :return:
    '''
    with open('../data/user_settings.json') as file:
        data = json.load(file)
        utils_log.debug(f'Делай раз. Прием: {data}')
    if type == 'valut':
        for key, value in data.items():
            if key == "user_currencies":
                list_answer = value
    if type == 'stock':
        for key, value in data.items():
            if key == "user_stocks":
                list_answer = value
    utils_log.debug(f'Делай два. Ответ функции: {list_answer}')
    return list_answer


def greet_function():
    answer_full = {}
    answer_full["greeting"] = (greeting_time())
    utils_log.debug(f'Делай ноль - контроль работы = {answer_full}')
    answer_full['cards'] = (cards_ful_answer(data_frame_work(), creat_list_cards(data_frame_work())))
    utils_log.debug(f'Делай два - контроль работы = {answer_full}')
    got = top_trans(data_frame_work())
    answer_full['top_transactions'] = got
    utils_log.debug(f'Делай три - контроль работы = {answer_full}')
    list_valute = list_paper('valut')
    answer_valut = choice_parer('valut', list_valute)
    answer_full["currency_rates"] = answer_valut
    list_stok = list_paper('stock')
    answer_stok = choice_parer('stock', list_stok)
    answer_full["stock_prices"] = answer_stok
    utils_log.debug(f'Делай пять - контроль работы = {answer_full}')
    return answer_full
