from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.dirname(osPath.abspath(__file__))))
sysPath.append(rootDirectory)

from drawdata import *
from priceparser import *
from drawdata import *
from handleprices import *
from modellingparameters import *
from predictionalgorithm import *

NEED_DRAW_IMPORTANCE_COEFFICITENT: bool = False
NEED_DRAW_FUTURE_PRICES_OF_ONE_CRYPTOCURRENCY: bool = False
NEED_DRAW_FUTURE_PRICES_OF_RANDOM_GRAPHIC: bool = False

CRYPTOCURRENCY_LIST: list[str] = ["IOTA", "CRV", "XLM", "BTC", "ETH"]

if __name__ == "__main__":
    if(NEED_DRAW_IMPORTANCE_COEFFICITENT):
        drawImportanceCoefficientOf(CRYPTOCURRENCY_LIST[0])

    elif(NEED_DRAW_FUTURE_PRICES_OF_ONE_CRYPTOCURRENCY):
        drawPredictionPricesOf(CRYPTOCURRENCY_LIST[0])

    elif(NEED_DRAW_FUTURE_PRICES_OF_RANDOM_GRAPHIC):
        drawPredictionPriceWithRandomValues(100.05, 132.2)

    else:
        handlePricesOf(CRYPTOCURRENCY_LIST, ParametersOnSmallDistances())
        handlePricesOf(CRYPTOCURRENCY_LIST, ParametersOnHugeDistance())