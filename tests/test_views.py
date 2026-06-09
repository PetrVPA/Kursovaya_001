from src.views import list_paper


def test_list_paper1():
    name = 'valut'
    stend = list_paper(name)
    assert stend == ['CNY', 'USD', 'EUR']


def test_list_paper2():
    name = 'stock'
    stend = list_paper(name)
    assert stend == ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
