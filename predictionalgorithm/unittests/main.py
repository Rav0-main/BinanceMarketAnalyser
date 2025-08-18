from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.dirname(osPath.abspath(__file__))))
sysPath.append(rootDirectory)

from drawdata import *
from handleprices import *
from modellingparameters import *
from predictionalgorithm import *

NEED_DRAW_IMPORTANCE_COEFFICITENT: bool = False
NEED_DRAW_FUTURE_PRICES_OF_ONE_CRYPTOCURRENCY: bool = False
NEED_DRAW_FUTURE_PRICES_OF_RANDOM_GRAPHIC: bool = False
NEED_DRAW_SET_PRICES: bool = False

CRYPTOCURRENCY_LIST: list[str] = ["SOL", "IOTA", "CRV", "XLM", "BTC", "ETH"]

if __name__ == "__main__":
    if(NEED_DRAW_IMPORTANCE_COEFFICITENT):
        drawImportanceCoefficientOf(CRYPTOCURRENCY_LIST[0])

    elif(NEED_DRAW_FUTURE_PRICES_OF_ONE_CRYPTOCURRENCY):
        drawPredictionPricesOf(CRYPTOCURRENCY_LIST[0])

    elif(NEED_DRAW_FUTURE_PRICES_OF_RANDOM_GRAPHIC):
        drawPredictionPriceWithRandomValues(100.05, 132.2)

    elif(NEED_DRAW_SET_PRICES):
        past: list[float] = [1, 2, 3, 6, 7, 8, 10, 9, 6, 7, 5, 4, 3, 1, 0.5, 1.5, 2, 4, 3, 2.5, 1.5, 0.8, 0.6, 0.3, 0.2, 0.8, 1.5, 2.3]
        future: int = len(past) + 10
        drawPredictionPricesOfSetValues(past, future)

    else:
        handlePricesOf(CRYPTOCURRENCY_LIST, ParametersOnSmallDistances())
        handlePricesOf(CRYPTOCURRENCY_LIST, ParametersOnHugeDistance())