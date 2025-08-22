from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from .cryptocurrencyinformation import CryptocurrencyInformation
from .jsonparser import CryptocurrencyJsonContentParser
from .priceprinter import PredictionPricesPrinter
from cryptocurrencymanager import CryptocurrencyManager
from executor import (ScreenExecutor,
                      ScreenOfLoggingOutputer)
from general import (FILE_NAME_WITH_CRYPTOCURRENCIES,
                     LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES)
from .strcommands import *
from os import system

class ManyPricesScreenExecutor(ScreenExecutor):
    """
    The second screen's executor receives information from the file and uses it to display information about the future prices for each cryptocurrency.
    """
    __cryptocurrencies: list[CryptocurrencyInformation]
    __cryptocurrencyManager: CryptocurrencyManager
    __cryptocurrencyJsonContentParser: CryptocurrencyJsonContentParser
    __predictionPricesPrinter: PredictionPricesPrinter
    _logging: bool

    def __init__(self, logging: bool):
        self.__cryptocurrencies = []
        self.__cryptocurrencyJsonContentParser = CryptocurrencyJsonContentParser()
        self.__cryptocurrencyManager = CryptocurrencyManager()
        self.__predictionPricesPrinter = PredictionPricesPrinter(self.__cryptocurrencyManager)
        self._logging = logging

    def execute(self) -> bool:
        system("cls")
        
        self.__parseJsonContent()
        self.__printAllPredictedPrice()
        
        print("Press <Enter> to continue.")
        input()
        return False

    def __parseJsonContent(self):
        self.__cryptocurrencies = self.__cryptocurrencyJsonContentParser.parse(FILE_NAME_WITH_CRYPTOCURRENCIES)

    def __printAllPredictedPrice(self):
        self.__predictionPricesPrinter.printPredictionPricesOf(self.__cryptocurrencies, self._logging)

class ManyPricesScreenViewerWithoutLogging(ManyPricesScreenExecutor):
    _logging = False

    def __init__(self):
        super().__init__(self._logging)

class ManyPricesScreenViewerWithLogging(ManyPricesScreenExecutor):
    _logging = True

    def __init__(self):
        super().__init__(self._logging)

class LoggingOutputerOfManyPricesViewerScreen(ScreenOfLoggingOutputer):
    def __init__(self):
        self._loggingFileName = LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES
        self._cryptocurrencyManager = CryptocurrencyManager()

class DocumentationScreenOfManyPricesViewer(ScreenExecutor):
    def __init__(self):
        pass

    def execute(self) -> bool:
        system("cls")
        print(f"Displays information about the prediction prices of the cryptocurrencies specified in {FILE_NAME_WITH_CRYPTOCURRENCIES}.")
        print()
        print(f"{FILE_NAME_WITH_CRYPTOCURRENCIES} parameter documentation: ")
        print()
        print(f"'{STRICT_COMMAND_CHECKING}' - 0 then, when an error is found, data extraction does not complete.")
        print(f"'{STRICT_COMMAND_CHECKING}' - 1 then, when an error is found, data extraction does complete.")
        print("--------------------------------------------------------------")
        print()
        print("For each next fields of:")
        print()
        print("'CRYPTOCURRENCY_SYMBOL' : { ")
        print(f"'{START_DATETIMES_COMMAND}' : list[str],")
        print(f"'{END_DATETIMES_COMMAND}' : list[str],")
        print(f"'{FUTURE_DATETIMES_COMMAND}' : list[str],")
        print(f"'{TIME_INTERVALS_COMMAND}' : list[str]")
        print("}")
        print()
        print(f"'{START_DATETIMES_COMMAND}' is list of start dates;")
        print(f"'{END_DATETIMES_COMMAND}' is list of end dates;")
        print(f"'{FUTURE_DATETIMES_COMMAND}' is list of future dates;")
        print(f"'{TIME_INTERVALS_COMMAND}' is list of time intervals.")
        print("--------------------------------------------------------------")
        print()
        print(" * 'start date' - is start date to parsing of price values.")
        print(" * 'end date' - is end date of parsing of price values.")
        print(" * 'future date' - is future date to predict.")
        print(" * 'time interval' - is time interval between price values in parsing data.")
        print()
        print("All dates must be in ISO format or relative format: 'now-ti' or 'now+ti' where ti - is time interval; for example now-30m, now+2h, now-1d.")
        print()
        print("Time interval must be in format: 5m, 30m, 2h, 1d and etc.")
        print("--------------------------------------------------------------")
        print()
        print("Parsing case is the corresponding data from each field taken under one index.")
        print("--------------------------------------------------------------")
        print()
        print("Example of BTC:")
        print()
        print('"BTC": {')
        print(f'"{START_DATETIMES_COMMAND}": ["now-7d", "now-31d"],')
        print(f'"{END_DATETIMES_COMMAND}": ["now", "now"],')
        print(f'"{FUTURE_DATETIMES_COMMAND}": ["now+1d", "now+7d"],')
        print(f'"{TIME_INTERVALS_COMMAND}": ["1h", "4h"]')
        print("}")
        print()
        print("In that variant two parsing cases: index=0 and index=1:")
        print("index=0: start date = 'now-7d', end date='now', future date='now+1d', time interval='1h';")
        print("index=1: start date = 'now-31d', end date='now+1d', future date='now+7d', time interval='4h'.")
        print()
        print("Press <Enter> to continue")
        input()
        return False