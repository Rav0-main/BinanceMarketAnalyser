from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

rootDirectory = osPath.dirname(rootDirectory)
sysPath.append(rootDirectory)

from .cryptocurrencyinformation import CryptocurrencyInformation
from priceparser import (PriceParserBinanceAPI,
                         getXYFormatFrom,
                         PriceInformation)
from predictionalgorithm import getPredictedFuturePricesIn
from datetime import datetime
from general import STR_DATE_FORMAT
from time import sleep

class PredictedPricePrinter:
    timeSleep: float = 2.0
    sleepCycle: int = 4
    def __init__(self):
        pass

    def printPredictedPricesOf(self, cryptocurrencies: list[CryptocurrencyInformation]):
        if(len(cryptocurrencies) == 0):
            print("Error. Not valid cryptocurrencies!")
            return
        
        for cryptocurrency in cryptocurrencies:
            self.__printPredictedPricesOfOneCryptocurrency(cryptocurrency)

    def __printPredictedPricesOfOneCryptocurrency(self, cryptocurrency: CryptocurrencyInformation):
        priceParser = PriceParserBinanceAPI(cryptocurrency.symbol)
        print(f"PREDICTION: {cryptocurrency.symbol.upper()}")
        print("=================================================================")

        for start, end, future, timeInterval, i in zip(cryptocurrency.startDatetimes,
            cryptocurrency.endDatetimes, cryptocurrency.futureDatetimes,
            cryptocurrency.timeIntervals, range(1, len(cryptocurrency.startDatetimes)+1)
            ):

            priceParser.timeInterval = timeInterval[0]
            priceParser.priceCount = int((end.timestamp()-start.timestamp())*1000) // timeInterval[1]
            prices: list[PriceInformation] = priceParser.getPricesByProperties(start, end)
            openPrices, closePrices = getXYFormatFrom(prices)
            lastOpenPrice: tuple[int, float] = openPrices[-1]
            lastClosePrice: tuple[int, float] = closePrices[-1]

            futureDatetime: int = int(future.timestamp() * 1000)
            futureOpenPrices = getPredictedFuturePricesIn(openPrices, futureDatetime)
            futureClosePrices = getPredictedFuturePricesIn(closePrices, futureDatetime)

            print("-----------------------------------------------------------------")
            self.__printDatetimeInformation((start, end), timeInterval[0])

            startInformation: str = "1. Open Price"
            self.__printInformationAboutFuturePrice(startInformation, futureOpenPrices[-1], lastOpenPrice)

            startInformation = "2. Close Price"
            self.__printInformationAboutFuturePrice(startInformation, futureClosePrices[-1], lastClosePrice)

            if(i % self.sleepCycle == 0):
                sleep(self.timeSleep)

        print("=================================================================")
        sleep(self.timeSleep)

    def __printDatetimeInformation(self, datetimeInterval: tuple[datetime, datetime], timeInterval: str):
        print("Datetime interval:")
        print(f"From {datetimeInterval[0].strftime(STR_DATE_FORMAT)} to {datetimeInterval[1].strftime(STR_DATE_FORMAT)}")
        print(f"Time interval: {timeInterval}")

    def __printInformationAboutFuturePrice(self, startInformation: str, futurePrice: tuple[int, float], pastPrice: tuple[int, float]):
        print(startInformation)
        
        pastDatetime: str = datetime.fromtimestamp(pastPrice[0]/1000).strftime(STR_DATE_FORMAT)
        futureDatetime: str = datetime.fromtimestamp(futurePrice[0]/1000).strftime(STR_DATE_FORMAT)

        print(f"Price from {pastPrice[1]:.3f} ({pastDatetime}) move to {futurePrice[1]:.3f} ({futureDatetime})")
        print(f"The relative change is: {(futurePrice[1] - pastPrice[1])/futurePrice[1]*100:.3f}%")