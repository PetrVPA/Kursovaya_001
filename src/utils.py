import logging
from datetime import date
from src.views import stock_cost
from src.views import valute_cost

import pandas as pd
from datetime import datetime


utils_log = logging.getLogger('utils')
file_utils_log = logging.FileHandler(r'..\data\utils.log', encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


def choice_parer(type:str, list_reqwest:list)-> dict:
    '''
    функция принимает тип строки 'stock' или 'valut' и список тикеров (перечень необходимых) в соответствии с типом
     и возвращает список валют либо акций для формирования главного ответа.
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
            base = valute_cost(item)
            setr[item] = base
            avane.append(setr[item])
        answer["currency"] = setr
    utils_log.debug(f'Делей раз - список бумаг - {answer}')
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


def data_frame_work()-> pd.DataFrame:
    #создаем дата фрейм для работы с данными
    excel_data = pd.read_excel(r"..\data\operations.xlsx")
    utils_log.debug(f'Делей раз - главный датафрейм курсового проекта - {excel_data}')
    return excel_data

def creat_list_cards(card_data:pd.DataFrame)-> list:
    '''
    функция принимает дата фрейм транзакций принмает все значения карт в множество и возвращает список банковских карт
    участвующих в тарнз акциях
    :param card_data:
    :return:
    '''
    # Формируем датафрейм без пустых элементов содержащихся в столбце "Номер карты"
    cards = card_data.loc[card_data['Номер карты'].notnull()]
    #формируем множество () через фильтрацию с выбором столбца "Номер карты"
    cards_set = set(cards['Номер карты'].tolist())
    # возвращаем перечень кар преобразовав его из множества в список
    utils_log.debug(f'Делей раз - список банковских карт = {cards_set}')
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
    output={}
    for item in name_cards:
        #определяем словарь для финального ответа курсового проекта по банковским картам
        answer = {}
        #убираем звездочку из ответа
        stok = item[1:]
        #заносим первый ключ со значением в словарь
        answer["last_digits"] = stok
        #формируем датафрейм для выбранной карты
        spred = card_data.loc[card_data['Номер карты'] == item]
        #находим сумму по всем платежам карты
        money = spred['Сумма платежа'].sum()
        #убираем лишние знаки после запятой
        money = f'{money:.2f}'
        #возвращаем значению тип float
        money = float(money)
        #заносим второй ключ ответа по картам
        answer["total_spent"] = money
        #вычисляем кэш бек из условия курсовой работы равен 1% от общей суммы
        cash_back = money * 0.01
        # убираем лишние знаки после запятой
        cash_back = f'{cash_back:.2f}'
        # возвращаем значению тип float
        cash_back = float(cash_back)
        # заносим третий ключ ответа по картам
        answer["cash_back"] = cash_back
        utils_log.debug(f'итоговый словарь = {answer}')
        #добавляем словарь в финальный список по картам
        shtorm.append(answer)
        output ["cards"] = shtorm
        utils_log.debug(f'добавляем в список = {shtorm}')
        utils_log.debug(f'Итоговый ответ в формате курсового проекта = {output}')
    return output


def top_trans (data:pd.DataFrame)-> pd.DataFrame:
    # Получаем сегодняшнюю дату
    today = date.today()
    # Формируем формат выдаваемый
    formatted_date = today.strftime("%Y-%m-%d")
    # узнаем день месяца
    today_date = today.day
    # узнаем месяц
    today_month = today.month
    # приводим столбец к формату datetime64
    data['Дата платежа'] = pd.to_datetime(data['Дата платежа'], dayfirst=True)
    # выбираем из датафрейма нужный промежуток с 1 по текущее и подменой года по сохраненный файл...
    spred = data.loc[(data['Дата платежа'] <= f'2021-{today_month}-{today_date}') & (
                data['Дата платежа'] >= f'2021-{today_month}-1')]
    # сортировка по возрастанию с 1 по текущее число
    spred = spred.sort_values(by='Дата платежа', ascending=True)
    spred['Сумма платежа'] = spred['Сумма платежа'].apply(lambda x: abs(x) if x < 0 else x)
    # вывод нескольких конкретных столбов
    spred = spred.sort_values(by='Сумма платежа', ascending=False)
    utils_log.debug(f'Итоговый ответ в формате курсового проекта = {spred}')
    return spred

