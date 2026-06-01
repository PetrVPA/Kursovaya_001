import requests
import logging
import json




view_log = logging.getLogger('view')
file_view_log = logging.FileHandler(r'..\data\viewlog.log', encoding='utf-8')
view_log.addHandler(file_view_log)
file_view_log_formater = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
file_view_log.setFormatter(file_view_log_formater)
view_log.setLevel(logging.DEBUG)


def valute_cost(name_valute:str) -> float:
    '''
    функция принимает трикер валюты возвращает стоимость валюты в рублях
    :param name_valute трикер валюты
    :return: stend возвращаемое значение стоимости валюты
    '''
    name_valute = name_valute.upper()
    try:
        response = requests.get(  'https://www.cbr-xml-daily.ru/daily_json.js', 'GET', timeout=15)
        view_log.debug(f'Делай раз - чтение прошло успешно и записано \n {response.text}')
    except requests.exceptions. Timeout:
        print("Превышено время ожидания...")
    except requests.exceptions.TooManyRedirects:
        print("Количество перенаправлений превысело предел")
    except requests.exceptions.RequestException:
        print("Ошибка в обращении к сервису. Попробуте позже")
    else:
        stend = json.loads(response.text)
        view_log.debug(f'Делай два - принят словарь \n {stend}')
        stend = stend['Valute'][name_valute]['Previous']
        stend = f'{stend:.2f}'
        view_log.debug(f'Делай три - ответ функции \n {stend}')

    return stend


def stock_cost(name_stock: str) -> float:
    '''
    Функция принимает строку с трикером 1-й акции и возвращает ее стоимость
    :param name_stock:
    :return:
    '''
    name_stock = name_stock.upper()
    #url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={name_stock}&interval=5min&apikey=KGGQKNFNRO6HY5MP'
    #url = f'https://www.alphavantage.co/query?function = TIME_SERIES_DAILY&symbol={name_stock}&interval=5min&apikey=KGGQKNFNRO6HY5MP'
    try:
        #data = requests.get(url, timeout=1500).json()
        data = {'timestamp': '2026-05-22 19:55:00', 'open': 252.030, 'high': 252.2197, 'low': 525.0000,
                'close': 252.1218, 'volume': 6458}
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
        view_log.debug(f'Делай раз. Что получили с сервера: {data}')
        #подмена данных с сайта не дающего инфу в его формате

        out = data['close']
        out = f'{out:.2f}'
        view_log.debug(f'Делай два. Ответ функции: {name_stock} = {out}')

    return out

#Сомнительное решение:
def list_paper(type:str) -> list:
    '''
    функция принимает строковое значение выбора валюты 'valut' или акции 'stock' и выдает список либо валют либо акций
    из файла настройки пользователя data/user_settings.json где содержится эта информация.
    :param type:
    :return:
    '''
    with open('../data/user_settings.json') as file:
        data = json.load(file)
        view_log.debug(f'Делай раз. Прием: {data}')
    if type == 'valut':
        for key, value in data.items():
            if key == "user_currencies":
                list_answer = value
    if type == 'stock':
        for key, value in data.items():
            if key == "user_stocks":
                list_answer = value
    view_log.debug(f'Делай два. Ответ функции: {list_answer}')
    return list_answer
