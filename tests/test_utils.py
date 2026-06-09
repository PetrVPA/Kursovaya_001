from unittest.mock import patch
from datetime import datetime

from src.utils import greeting_time
from src.utils import data_frame_work
from src.utils import creat_list_cards
from src.utils import cards_ful_answer


def test_greeting_time1():
    test_time = datetime(2026, 6, 9, 10, 50, 7)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = test_time
        assert greeting_time() == "Доброе утро"


def test_greeting_time2():
    test_time = datetime(2026, 6, 9, 13, 50, 7)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = test_time
        assert greeting_time() == "Добрый день"


def test_greeting_time3():
    test_time = datetime(2026, 6, 9, 19, 50, 7)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = test_time
        assert greeting_time() == "Добрый вечер"


def test_greeting_time4():
    test_time = datetime(2026, 6, 9, 0, 50, 7)
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = test_time
        assert greeting_time() == "Доброй ночи"


def test_creat_list_cards():
    data = data_frame_work()
    assert creat_list_cards(data) == ['*1112', '*4556', '*5091', '*5441', '*5507', '*6002', '*7197']


answer_001 = {'cards': [{'last_digits': '1112', 'total_spent': 46207.08, 'cash_back': 462.07}]}
answer_002 = {'cards': [{'last_digits': '4556', 'total_spent': 4094249.17, 'cash_back': 40942.49}]}
answer_003 = {'cards': [{'last_digits': '1112', 'total_spent': 46207.08, 'cash_back': 462.07},
                        {'last_digits': '4556', 'total_spent': 4094249.17, 'cash_back': 40942.49},
                        {'last_digits': '5091', 'total_spent': 19816.84, 'cash_back': 198.17},
                        {'last_digits': '5441', 'total_spent': 470854.8, 'cash_back': 4708.55},
                        {'last_digits': '5507', 'total_spent': 84000.0, 'cash_back': 840.0},
                        {'last_digits': '6002', 'total_spent': 69200.0, 'cash_back': 692.0},
                        {'last_digits': '7197', 'total_spent': 2557824.54, 'cash_back': 25578.25}]}


def test_cards_ful_answer1():
    data = data_frame_work()
    name_cards = ['*1112']
    pops = cards_ful_answer(data, name_cards)
    assert pops == answer_001


def test_cards_ful_answer2():
    data = data_frame_work()
    name_cards = ['*4556']
    pops = cards_ful_answer(data, name_cards)
    assert pops == answer_002


def test_cards_ful_answer3():
    data = data_frame_work()
    name_cards = ['*1112', '*4556', '*5091', '*5441', '*5507', '*6002', '*7197']
    pops = cards_ful_answer(data, name_cards)
    assert pops == answer_003
