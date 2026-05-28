from src.views import function_cost_valut
from src.utils import read_json_stock
from src.views import stock_cost2
from src.utils import greeting_time

if __name__ == "__main__":
    # name_valut = 'EUR'
    # cels = function_cost_valut(name_valut)
    # print(cels)
    name_stock = 'AMZN'
    cels = stock_cost2(name_stock)
    print(cels)
    # print(greeting_time())
