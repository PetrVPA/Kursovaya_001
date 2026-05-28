import json
import logging
from unittest.mock import inplace

import pandas as pd
from datetime import datetime

utils_log = logging.getLogger('utils')
file_utils_log = logging.FileHandler('utils.log', encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


def read_json_valut(input_data:list[dict], name_valut: str)-> float:
    '''
    функция принимает список словарей с данными по валютам, и трикет валюты например 'USD' и возвращает стоимость в
    рублях float.
    :param input_data:
    :param name_valut:
    :return:
    '''
    valute_data = input_data['Valute']
    utils_log.debug(f'Принимает словарь - {valute_data}')
    previous_value = valute_data[f'{name_valut}']['Previous']
    utils_log.debug(f'Возвращает значение - {previous_value}')
    return previous_value


def read_json_stock(input_data: dict)-> float:
    '''
    функция принимает список словарь с данными по акции и возвращает стоимость в float.
    :param input_data:
    :param name_valut:
    :return:
    '''
    utils_log.debug(f'Получил инфу - {input_data}')
    stock_value = input_data['close']
    utils_log.debug(f'Стоимость акции - {stock_value}')
    return stock_value

def answer_parer(type:str, list_reqwest:list)-> dict:
    '''
    функция принимает тип строки 'stock' или 'valut' и список тикеров в соответствии с типом и возвращает список валют
    либо  акций для формирования главного ответа.
    :param type:
    :param list_reqwest:
    :return:
    '''
    answer ={}
    setr = {}
    avane =[]
    if type == 'stock':
        for item in list_reqwest:
            base = stock_cost(item)
            setr[item] = base
            avane.append(setr[item])
        answer["stock prices"] = setr
    if type == 'valut':
        for item in list_reqwest:
            base = stock_cost(item)
            setr[item] = base
            avane.append(setr[item])
        answer["currency"] = setr
    return answer

def greeting_time() -> str:
    '''
    функция здоровается в зависимости от текущего времени суток
    :return:
    '''
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


def data_frame_info()-> pd.DataFrame:
    #создаем дата фрейм для работы с данными
    excel_data = pd.read_excel("..\data\operations.xlsx")
    return excel_data

def card_set(card_data:pd.DataFrame)-> list:
    '''
    функция принимает дата фрейм транзакций принмает все значения карт в множество и возвращает список банковских карт
    участвующих в тарнз акциях
    :param card_data:
    :return:
    '''
    cards = card_data.loc[card_data['Номер карты'].notnull()]
    cards_set = set(cards['Номер карты'].tolist())
    return list(cards_set)

def cards_ful_answer(card_data:pd.DataFrame, name_cards:list)-> list(dict):
    '''
    функция принимает дата фрейм и список банковских карт и возвращает список словарей в формате определенном заданием
     курсового проекта
    :param card_data:
    :param name_cards:
    :return:
    '''
    shtorm = []
    for item in name_cards:
        answer = {}
        stok = item[1:]
        answer["last_digits"] = stok
        spred = card_data.loc[card_data['Номер карты'] == item]
        money = spred['Сумма платежа'].sum()
        money = f'{money:.2f}'
        money = float(money)
        answer["total_spent"] = money
        cash_back = money * 0.01
        cash_back = f'{cash_back:.2f}'
        cash_back = float(cash_back)
        answer["cash_back"] = cash_back
        utils_log.debug(f'итоговый словарь = {answer}')
        shtorm.append(answer)
        utils_log.debug(f'добавляем в список = {shtorm}')

    return shtorm

