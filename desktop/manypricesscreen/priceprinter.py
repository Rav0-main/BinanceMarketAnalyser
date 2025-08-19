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
from general import (STR_DATE_FORMAT,
                     LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES,
                     FILE_NAME_WITH_CRYPTOCURRENCIES)
from time import sleep

class PredictedPricePrinter:
    __timeSleep: float = 2.0
    __sleepCycle: int = 4

    __loggingBySymbols: dict[str, str] = {}
    __firstDashLine: str = "================================================================="
    __secondDashLine: str = "-----------------------------------------------------------------"

    __loggingInformation: str = ""

    def __init__(self):
        pass

    def printPredictedPricesOf(self, cryptocurrencies: list[CryptocurrencyInformation], logging: bool):
        if(len(cryptocurrencies) == 0):
            print("Error. Not valid cryptocurrencies!")
            return
        
        for cryptocurrency in cryptocurrencies:
            self.__printPredictedPricesOfOneCryptocurrency(cryptocurrency, logging)

        if(not logging):
            return
        
        loggingResult: str = f"{FILE_NAME_WITH_CRYPTOCURRENCIES} log.\nDatetime moment: {datetime.now().strftime(STR_DATE_FORMAT)}.\n{self.__firstDashLine}\n"
        for cryptocurrency in self.__loggingBySymbols.keys():
            loggingResult = loggingResult + self.__loggingBySymbols[cryptocurrency]

        with open(LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES, "w") as file:
            file.write(loggingResult)

    def __printPredictedPricesOfOneCryptocurrency(self, cryptocurrency: CryptocurrencyInformation, logging: bool):
        priceParser = PriceParserBinanceAPI(cryptocurrency.symbol)
        
        print(f"PREDICTION: {cryptocurrency.symbol}")
        print(self.__firstDashLine)

        self.__loggingInformation: str = f"PREDICTION: {cryptocurrency.symbol}.\n{self.__firstDashLine}\n"

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

            if(i != 1):
                print(self.__secondDashLine)
            if(i != 1):
                self.__loggingInformation = self.__loggingInformation + self.__secondDashLine + "\n"

            self.__printDatetimeInformation((start, end), timeInterval[0])

            startInformation: str = "1. Open Price"
            self.__loggingInformation = self.__loggingInformation + "1. Open Price:\n"
            self.__printInformationAboutFuturePrice(startInformation, futureOpenPrices[-1], lastOpenPrice)

            startInformation = "2. Close Price"
            self.__loggingInformation = self.__loggingInformation + "2. Close Price:\n"
            self.__printInformationAboutFuturePrice(startInformation, futureClosePrices[-1], lastClosePrice)

            if(i % self.__sleepCycle == 0):
                sleep(self.__timeSleep)

        print(self.__firstDashLine)
        self.__loggingInformation = self.__loggingInformation + self.__firstDashLine + "\n"
        
        if(logging):
            self.__loggingBySymbols[cryptocurrency.symbol] = self.__loggingInformation
        self.__loggingInformation = ""

        sleep(self.__timeSleep)

    def __printDatetimeInformation(self, datetimeInterval: tuple[datetime, datetime], timeInterval: str):
        print("Datetime interval:")
        print(f"From {datetimeInterval[0].strftime(STR_DATE_FORMAT)} to {datetimeInterval[1].strftime(STR_DATE_FORMAT)}")
        print(f"Time interval: {timeInterval}")

        self.__loggingInformation = self.__loggingInformation + f"Datetime interval: {datetimeInterval[0].strftime(STR_DATE_FORMAT)} - {datetimeInterval[1].strftime(STR_DATE_FORMAT)}.\nTime interval: {timeInterval}.\n"

    def __printInformationAboutFuturePrice(self, startInformation: str, futurePrice: tuple[int, float], pastPrice: tuple[int, float]):
        print(startInformation)
        
        pastDatetime: str = datetime.fromtimestamp(pastPrice[0]/1000).strftime(STR_DATE_FORMAT)
        futureDatetime: str = datetime.fromtimestamp(futurePrice[0]/1000).strftime(STR_DATE_FORMAT)

        print(f"Price from {pastPrice[1]:.3f}$ ({pastDatetime}) move to {futurePrice[1]:.3f}$ ({futureDatetime})")
        print(f"Relative precent: {(futurePrice[1] - pastPrice[1])/pastPrice[1]*100:.3f}%")

        self.__loggingInformation = self.__loggingInformation + f"Predict on datetime: {futureDatetime}.\n"
        self.__loggingInformation = self.__loggingInformation + f"Price from {pastPrice[1]:.3f}$ ({pastDatetime}) move to {futurePrice[1]:.3f}$ ({futureDatetime}).\n" + f"Relative precent: {(futurePrice[1] - pastPrice[1])/pastPrice[1]*100:.3f}%.\n"