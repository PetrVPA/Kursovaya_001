import logging
from datetime import date
import json


import pandas as pd
from datetime import datetime
import os.path
import requests
from dotenv import load_dotenv

file_path = os.path.join(r'..\data\utils.log')
log_path = os.path.abspath(file_path)
utils_log = logging.getLogger('utils')
file_utils_log = logging.FileHandler(log_path, encoding='utf-8')
utils_log.addHandler(file_utils_log)
file_utils_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_utils_log.setFormatter(file_utils_log_formater)
utils_log.setLevel(logging.DEBUG)


def choice_parer(type: str, list_reqwest: list) -> dict:
    '''
    функция принимает тип строки 'stock' или 'valut' и список тикеров (перечень необходимых) в соответствии с типом
     и возвращает список валют либо акций для формирования главного ответа.
    :param type: принимает переменную что нужно валюта либо акции
    :param list_reqwest: принимает трикеры либо валют, либо акций
    :return: возвращает словарь со стоимостью валют либо акций
    '''
    avane = []
    if type == 'stock':
        for item in list_reqwest:
            setr = {}
            base = stock_cost(item)
            setr['stock'] = item
            setr['price'] = base
            avane.append(setr)

    if type == 'valut':
        for item in list_reqwest:
            setr = {}
            base = valute_cost(item)
            setr['currency'] = item
            setr['rate'] = base
            avane.append(setr)
    utils_log.debug(f'Делей раз - список бумаг - {avane}')
    return avane


def greeting_time() -> str:
    '''
    функция здоровается в зависимости от текущего времени суток
    :return: возвращает актуальное приветствие
    '''
    current_datetime = datetime.now()
    hour_current = current_datetime.hour

    if hour_current >= 6 and hour_current < 12:
        greeting = "Доброе утро"
        utils_log.debug(f'Делай раз - сейчас утро? - {greeting}, {current_datetime}.')
    if hour_current >= 12 and hour_current < 18:
        greeting = "Добрый день"
        utils_log.debug(f'Делай два - сейчас день? - {greeting}, {current_datetime}.')
    if hour_current >= 18 and hour_current <= 23:
        greeting = "Добрый вечер"
        utils_log.debug(f'Делай три - сейчас вечер? - {greeting}, {current_datetime}.')
    if hour_current >= 0 and hour_current < 6:
        greeting = "Доброй ночи"
        utils_log.debug(f'Делай четыре - сейчас ночь? - {greeting}, {current_datetime}.')

    return greeting


def data_frame_work() -> pd.DataFrame:
    '''
    Возвращает в программу транзакции в виде дата фрейма из файла
    :return: дата фрейм транзакций
    '''
    #создаем дата фрейм для работы с данными
    file_path = os.path.join(r'..\data\operations.xlsx')
    set_path = os.path.abspath(file_path)
    excel_data = pd.read_excel(set_path)
    utils_log.debug(f'Делай раз - главный датафрейм курсового проекта - {excel_data}')
    return excel_data


def creat_list_cards(card_data: pd.DataFrame) -> list:
    '''
    функция принимает дата фрейм транзакций выбирает все значения карт в множество и возвращает список банковских карт
    участвующих в транзакциях
    :param card_data: датафрейм всех транзакций
    :return:список банковских карт участвующих в транзакциях
    '''
    # Формируем датафрейм без пустых элементов содержащихся в столбце "Номер карты"
    cards = card_data.loc[card_data['Номер карты'].notnull()]
    #формируем множество () через фильтрацию с выбором столбца "Номер карты"
    cards_set = set(cards['Номер карты'].tolist())
    cards_list = sorted(cards_set)
    # возвращаем перечень кар преобразовав его из множества в список
    utils_log.debug(f'Делай раз - список банковских карт = {cards_list}')
    return list(cards_list)


def cards_ful_answer(card_data: pd.DataFrame, name_cards: list) -> list[dict]:
    '''
    функция принимает дата фрейм и список банковских карт и возвращает список словарей в формате определенном заданием
     курсового проекта карта -> номер карты; расходы по карте; кэш бек
    :param card_data: дата фрейм
    :param name_cards: список банковских карт
    :return: список словарей
    '''
    shtorm = []
    for item in name_cards:
        #определяем словарь для финального ответа курсового проекта по банковским картам
        answer = {}
        #убираем звездочку из ответа
        stok = item[1:]
        #заносим первый ключ со значением в словарь
        answer["last_digits"] = stok
        #формируем датафрейм для выбранной карты
        spred = card_data.loc[card_data['Номер карты'] == item]
        spred['Сумма платежа'] = spred['Сумма платежа'].apply(lambda x: abs(x) if x < 0 else x)
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
        utils_log.debug(f'Итоговый ответ в формате курсового проекта = {shtorm}')
    return shtorm


def top_trans(data: pd.DataFrame) -> list[dict]:
    """
    Функция демонстрирует 5 топ транзакций по сумме платежа с указанием даты, категории и описания транзакции
    data: pd.DataFrame датафрейм всех операций
    storm возвращает список словарей топ 5 транзакций по сумме платежа
    """
    # Получаем сегодняшнюю дату
    today = date.today()
    # узнаем день месяца
    today_date = today.day
    # узнаем месяц
    today_month = today.month
    # приводим столбец к формату datetime64
    data['Дата платежа'] = pd.to_datetime(data['Дата платежа'], dayfirst=True)
    # выбираем из датафрейма нужный промежуток с 1 по текущее и подменой года по сохраненный файл...
    spred = data.loc[(data['Дата платежа'] <= f'2021-{today_month}-{today_date}') & (data['Дата платежа']
                                                                                     >= f'2021-{today_month}-1')]
    # сортировка по возрастанию с 1 по текущее число
    spred = spred.sort_values(by='Дата платежа', ascending=True)
    # убираем знак минус
    spred['Сумма платежа'] = spred['Сумма платежа'].apply(lambda x: abs(x) if x < 0 else x)
    # вывод нескольких конкретных столбов
    spred = spred.sort_values(by='Сумма платежа', ascending=False)
    utils_log.debug(f'Итоговый дата фрейм = {spred}')
    answer = spred.loc[:, ['Дата платежа', 'Сумма платежа', 'Категория', 'Описание']]
    answer = answer.head(5)
    answer = answer.rename(columns={'Дата платежа': 'date'})
    answer = answer.rename(columns={'Сумма платежа': 'amout'})
    answer = answer.rename(columns={'Категория': 'category'})
    answer = answer.rename(columns={'Описание': 'description'})
    answer['date'] = answer['date'].dt.strftime('%Y-%m-%d')
    storm = answer.to_dict('records')
    return storm


def valute_cost(name_valute: str) -> float:
    '''
    функция принимает трикер валюты возвращает стоимость валюты в рублях
    :param name_valute трикер валюты
    :return: stend возвращаемое значение стоимости валюты
    '''
    name_valute = name_valute.upper()
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js', 'GET', timeout=15)
        utils_log.debug(f'Делай раз - чтение прошло успешно и записано \n {response.text}')
    except requests.exceptions. Timeout:
        print("Превышено время ожидания...")
    except requests.exceptions.TooManyRedirects:
        print("Количество перенаправлений превысело предел")
    except requests.exceptions.RequestException:
        print("Ошибка в обращении к сервису. Попробуте позже")
    else:
        stend = json.loads(response.text)
        utils_log.debug(f'Делай два - принят словарь \n {stend}')
        stend = stend['Valute'][name_valute]['Previous']
        stend = f'{stend:.2f}'
        utils_log.debug(f'Делай три - ответ функции \n {stend}')

    return stend


def stock_cost(name_stock: str) -> float:
    '''
    Функция принимает строку с трикером 1-й акции и возвращает ее стоимость
    :param name_stock:
    :return:
    '''
    load_dotenv('../.env')
    api_token = os.getenv('API_KEY')
    name_stock = name_stock.upper()
    url = 'https://api.api-ninjas.com/v1/stockprice'
    API_KEY = api_token

    try:
        data = requests.get(
            url,
            params={'ticker': name_stock},
            headers={'X-Api-Key': API_KEY},
            timeout=10
        )

        data = data.json()
    except requests.exceptions.Timeout as timeout_err:
        return f"Превышено время ожидания...{timeout_err}"
    except requests.exceptions.HTTPError as http_err:
        return f"Код ошибки...{http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Ошибка соединения...{conn_err}"
    except requests.exceptions.TooManyRedirects:
        return "Количество перенаправлений превысело предел"
    except requests.exceptions.RequestException as req_err:
        return f"Ошибка в обращении к сервису. Попробутйе позже {req_err}"
    else:
        utils_log.debug(f'Делай раз. Что получили с сервера: {data}')
        out = data['price']
        out = f'{out:.2f}'
        utils_log.debug(f'Делай два. Ответ функции: {name_stock} = {out}')

    return out
