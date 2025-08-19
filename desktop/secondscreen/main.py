from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

rootDirectory = osPath.dirname(rootDirectory)
sysPath.append(rootDirectory)

from .cryptocurrencyinformation import CryptocurrencyInformation
from .jsonparser import CryptocurrencyJsonContentParser
from .priceprinter import PredictedPricePrinter
from executor import ScreenExecutor
from general import FILE_NAME_WITH_CRYPTOCURRENCIES

class SecondScreenExecutor(ScreenExecutor):
    """
    The second screen's executor receives information from the file and uses it to display information about the future prices for each cryptocurrency.
    """
    __cryptocurrencies: list[CryptocurrencyInformation] = []

    def __init__(self):
        pass

    def execute(self) -> bool:
        self.__parseJsonContent()
        self.__printAllPredictedPrice()
        print("Press <Enter> to continue.")
        input()
        return False

    def __parseJsonContent(self):
        self.__cryptocurrencies = CryptocurrencyJsonContentParser().parse(FILE_NAME_WITH_CRYPTOCURRENCIES)

    def __printAllPredictedPrice(self):
        PredictedPricePrinter().printPredictedPricesOf(self.__cryptocurrencies)