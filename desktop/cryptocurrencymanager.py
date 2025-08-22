from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from priceparser import (PriceParserBinanceAPI,
                         PriceInformation,
                         getXYFormatFrom)
from predictionalgorithm import getPredictionPricesIn
from datetime import (datetime,
                      timedelta)
from requests import HTTPError
from dataclasses import dataclass

@dataclass
class CryptocurrencyInputParseProtocol:
    cryptocurrencySymbol: str
    """
    For example, bitcoin - BTC, ethereum - ETH and etc.
    """

    datetimeInterval: tuple[datetime, datetime]
    """
    datetimeInterval[0] - start date\n
    datetimeInterval[1] - end date
    """

    timeInterval: tuple[str, int]
    """
    timeInterval[0] - time interval in string, for example "5m", "1h", "2d" and etc.
    timeInterval[1] - time interval in milliseconds
    """

@dataclass
class CryptocurrencyInputPredictProtocol(CryptocurrencyInputParseProtocol):
    datetimeToPredict: datetime

@dataclass
class CryptocurrencyOutputPredictProtocol:
    parsedPrices: list[PriceInformation]

    lastParsedOpenPriceInTimestamp: tuple[int, float]
    lastParsedClosePriceInTimestamp: tuple[int, float]
    
    predictionOpenPricesInTimestamp: list[tuple[int, float]]
    predictionClosePricesInTimestamp: list[tuple[int, float]]
    
class CryptocurrencyManager:
    __parser: PriceParserBinanceAPI
    
    def __init__(self):
        self.__parser: PriceParserBinanceAPI = PriceParserBinanceAPI("NULL")

    def existsOnMarket(self, cryptocurrencySymbol: str) -> bool:
        self.__parser.cryptocurrencySymbol = cryptocurrencySymbol
        startDatetime: datetime = datetime.now()-timedelta(hours=1)
        endDatetime: datetime = datetime.now()
        self.__parser.timeInterval = "30m"
        self.__parser.priceCount = 2
    
        try:
            self.__parser.getPricesByProperties(startDatetime, endDatetime)
            return True
        except HTTPError:
            return False
        
    def predict(self, protocol: CryptocurrencyInputPredictProtocol):
        prices = self.parse(protocol)
    
        openPrices, closePrices = getXYFormatFrom(prices)
        
        lastOpenPrice: tuple[int, float] = openPrices[-1]
        lastClosePrice: tuple[int, float] = closePrices[-1]

        datetimeToPredict: int = int(protocol.datetimeToPredict.timestamp() * 1000)
        predictionOpenPrices = getPredictionPricesIn(openPrices, datetimeToPredict)
        predictionClosePrices = getPredictionPricesIn(closePrices, datetimeToPredict)

        return CryptocurrencyOutputPredictProtocol(
            prices, lastOpenPrice, lastClosePrice, predictionOpenPrices, predictionClosePrices
        )
    
    def parse(self, protocol: CryptocurrencyInputParseProtocol) -> list[PriceInformation]:
        self.__parser.cryptocurrencySymbol = protocol.cryptocurrencySymbol
        self.__parser.timeInterval = protocol.timeInterval[0]
        self.__parser.priceCount = int(protocol.datetimeInterval[1].timestamp() -
                                       protocol.datetimeInterval[0].timestamp())*1000 \
                                       // protocol.timeInterval[1]
        prices: list[PriceInformation] = self.__parser.getPricesByProperties(protocol.datetimeInterval[0],
                                                                             protocol.datetimeInterval[1])

        return prices        
