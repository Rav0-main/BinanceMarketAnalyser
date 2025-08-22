from requests import get as httpsGet
from datetime import datetime
from dataclasses import dataclass

@dataclass
class PriceInformation:
    datetime: datetime
    open: float
    close: float

class NotSetPropertyException(Exception):
    pass

class PriceParserBinanceAPI:
    cryptocurrencySymbol: str
    timeInterval: str | None = None
    priceCount: int | None = None
    
    __API_URL: str = "https://api.binance.com/api/v3/klines"

    def __init__(self, cryptocurrencySymbol: str):
        self.cryptocurrencySymbol = cryptocurrencySymbol

    def getPricesByProperties(self, start: datetime, end: datetime) -> list[PriceInformation]:
        if(self.timeInterval == None):
            self.__raisePropertyNotInited("timeInterval")
        elif(self.priceCount == None):
            self.__raisePropertyNotInited("priceCount")

        startTime: datetime = start
        endTime: datetime = end

        requestParameters: dict[str, str | int] = {
            "symbol": self.cryptocurrencySymbol + "USDT",
            "interval": self.timeInterval,
            "limit": self.priceCount,
            "startTime": int(startTime.timestamp() * 1000),
            "endTime": int(endTime.timestamp() * 1000)
        }

        response = httpsGet(self.__API_URL, params=requestParameters)
        response.raise_for_status()

        data = response.json()

        result: list[PriceInformation] = []

        for position in data:
            timestamp: float = position[0] / 1000
            openPrice: float = float(position[1])
            closePrice: float = float(position[4])

            result.append(PriceInformation(datetime.fromtimestamp(timestamp),
                                           openPrice, closePrice))
            
        return result

    def __raisePropertyNotInited(self, propertyName: str):
        raise NotSetPropertyException(f"Property '{propertyName}' not set!")
    
def getXYFormatFrom(prices: list[PriceInformation]) -> tuple[list[tuple[int, float]], list[tuple[int, float]]]:
    """
    Returns (openPrices, closePrices) from 'prices'
    """
    openPrices: list[tuple[int, float]] = []
    closePrices: list[tuple[int, float]] = []

    timestamp: int = 0
    for price in prices:
        timestamp = int(price.datetime.timestamp() * 1000)
        openPrices.append((timestamp, price.open))
        closePrices.append((timestamp, price.close))

    return (openPrices, closePrices)