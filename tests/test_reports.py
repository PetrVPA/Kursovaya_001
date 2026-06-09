from unittest.mock import patch
import pandas as pd
from src.reports import spending_by_category
from src.utils import data_frame_work


data = {'Дата платежа': ['2018-02-26', '2018-02-13', '2018-01-05', '2018-01-04'],
        'Категория': ['Красота', 'Красота', 'Красота', 'Красота'], 'Сумма операции': [-2775.0, -145.0, -21.0, -316.0]}

row_labels = [6515, 6558, 6702, 6703]

zerro = pd.DataFrame(data=data, index=row_labels)
zerro['Дата платежа'] = pd.to_datetime(zerro['Дата платежа'])


def test_spending_by_category1():
    retro = data_frame_work()
    with patch('builtins.input', return_value='test_files'):
        result = spending_by_category(retro, 'Красота', '2018-3-4')
        result_sorted = result.sort_values(by='Дата платежа').reset_index(drop=True)
        zerro_sorted = zerro.sort_values(by='Дата платежа').reset_index(drop=True)
        pd.testing.assert_frame_equal(result_sorted, zerro_sorted)
