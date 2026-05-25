import json
import logging
from datetime import datetime

utils_log = logging.getLogger('utils')
file_utils_log = logging.FileHandler('utils.log', encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


def read_json_valut(input_data, name_valut)-> float:
    valute_data = input_data['Valute']
    utils_log.debug(f'Принимает словарь - {valute_data}')
    previous_value = valute_data[f'{name_valut}']['Previous']
    utils_log.debug(f'Возвращает значение - {previous_value}')
    return previous_value


def read_json_stock(input_data: dict)-> float:
    utils_log.debug(f'Получил инфу - {input_data}')
    stock_value = input_data['close']
    utils_log.debug(f'Стоимость акции - {stock_value}')
    return stock_value


def greeting_time() -> str:
    current_datetime = datetime.now()
    hour_current = current_datetime.hour

    if hour_current >= 6 and hour_current < 12:
        greeting = "Доброе утро"
        utils_log.debug(f'Делей раз - сейчас утро? - {greeting}')
    if hour_current >= 12 and hour_current < 18:
        greeting = "Добрый день"
        utils_log.debug(f'Делей два - сейчас день? - {greeting}')
    if hour_current >= 18 and hour_current <= 23:
        greeting = "Добрый вечер"
        utils_log.debug(f'Делей три - сейчас вечер? - {greeting}')
    if hour_current >= 0 and hour_current < 6:
        greeting = "Доброй ночи"
        utils_log.debug(f'Делей четыре - сейчас ночь? - {greeting}')

    return greeting