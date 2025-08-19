from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from .executor import ScreenExecutor
from .cryptocurrencychecker import cryptocurrencyExistsOnMarket
from .datetimeparser import (getTimeIntervalFrom,
                             getDatetimeFrom)
from .general import *
from priceparser import *
from predictionalgorithm import getPredictedFuturePricesIn
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from json import load as jsonLoad
from time import sleep

STRICT_COMMAND_CHECKING: str = "strict"
START_DATETIMES_COMMAND: str = "start-datetimes"
END_DATETIMES_COMMAND: str = "end-datetimes"
FUTURE_DATETIMES_COMMAND: str = "future-datetimes"
TIME_INTERVALS_COMMAND: str = "time-intervals"

@dataclass
class CryptocurrencyInformation:
    symbol: str
    startDatetimes: list[datetime]
    endDatetimes: list[datetime]
    futureDatetimes: list[datetime]
    timeIntervals: list[tuple[str, int]]

class SecondScreenExecutor(ScreenExecutor):
    cryptocurrencies: list[CryptocurrencyInformation] = []
    isStrictParsing: bool = True

    def __init__(self):
        pass

    def execute(self) -> bool:
        self.__parseJsonContent()
        self.__printAllPredictedPrice()
        return False

    def __parseJsonContent(self):
        self.cryptocurrencies = CryptocurrencyJsonContentParser().parse(FILE_NAME_WITH_CRYPTOCURRENCIES)

    def __printAllPredictedPrice(self):
        PredictedPricePrinter().printPredictedPricesOf(self.cryptocurrencies)
           
class CryptocurrencyJsonContentParser:
    isStrictParsing: bool = True
    cryptocurrencies: list[CryptocurrencyInformation] = []

    def __init__(self):
        pass

    def parse(self, fileName: str) -> list[CryptocurrencyInformation]:
        content: dict[str, Any] = self.__getJsonContentOf(fileName)

        if(STRICT_COMMAND_CHECKING in content and content[STRICT_COMMAND_CHECKING] == 0):
            self.isStrictParsing = False
        
        for symbol in content.keys():
            if(symbol == STRICT_COMMAND_CHECKING):
                continue

            print(f"Extracting {symbol} from {FILE_NAME_WITH_CRYPTOCURRENCIES}...")
            successParse: bool = self.__parseOneCryptocurrency(symbol, content[symbol])
            if(not successParse and self.isStrictParsing):
                return []
            elif(successParse):
                print("OK.")
            
        return self.cryptocurrencies

    def __parseOneCryptocurrency(self, symbol: str, information: dict[str, Any]) -> bool:
        """
        Returns True if symbol parsed success else False
        """
        if(not cryptocurrencyExistsOnMarket(symbol)):
            print(f"Error. Cryptocurrency not exists on market: {symbol}!")
            return False

        try:
            startDatetimeStrs: list[str] = information[START_DATETIMES_COMMAND]
        except KeyError:
            print(f"Error. In {symbol} - have not field: {START_DATETIMES_COMMAND}")
            return False

        try:
            endDatetimeStrs: list[str] = information[END_DATETIMES_COMMAND]
        except KeyError:
            print(f"Error. In {symbol} - have not field: {END_DATETIMES_COMMAND}")
            return False

        try:
            futureDatetimeStrs: list[str] = information[FUTURE_DATETIMES_COMMAND]
        except KeyError:
            print(f"Error. In {symbol} - have not field: {FUTURE_DATETIMES_COMMAND}")
            return False

        try:
            timeIntervalStrs: list[str] = information[TIME_INTERVALS_COMMAND]
        except KeyError:
            print(f"Error. In {symbol} - have not field: {TIME_INTERVALS_COMMAND}")
            return False

        try:
            startDatetimesLen: int = len(startDatetimeStrs)
        except TypeError:
            print(f"Error. In {symbol} - {START_DATETIMES_COMMAND} not a list!")
            return False

        try:
            endDatetimesLen: int = len(endDatetimeStrs)
        except TypeError:
            print(f"Error. In {symbol} - {END_DATETIMES_COMMAND} not a list!")
            return False

        try:
            futureDatetimesLen: int = len(futureDatetimeStrs)
        except TypeError:
            print(f"Error. In {symbol} - {FUTURE_DATETIMES_COMMAND} not a list!")
            return False

        try:
            timeIntervalsLen: int = len(timeIntervalStrs)
        except TypeError:
            print(f"Error. In {symbol} - {TIME_INTERVALS_COMMAND} not a list!")
            return False

        if(startDatetimesLen == endDatetimesLen and endDatetimesLen == futureDatetimesLen and futureDatetimesLen == timeIntervalsLen):
            validStartDatetimes: list[datetime] = []
            validEndDatetimes: list[datetime] = []
            validFutureDatetimes: list[datetime] = []
            validTimeIntervals: list[tuple[str, int]] = []
            
            for currentStartDatetime, currentEndDatetime, currentFutureDatetime, i in zip(
                map(getDatetimeFrom, startDatetimeStrs), map(getDatetimeFrom, endDatetimeStrs),
                map(getDatetimeFrom, futureDatetimeStrs), range(0, len(startDatetimeStrs))
                ):

                currentTimeInterval: tuple[str, int] = getTimeIntervalFrom(timeIntervalStrs[i],
                                                                                minutes=TimeIntervalValidDiapasons.minutes,
                                                                                hours=TimeIntervalValidDiapasons.hours,
                                                                                days=TimeIntervalValidDiapasons.days)
                if(currentStartDatetime >= currentEndDatetime):
                    print(f"Error. In {symbol} - {i+1}-th of {START_DATETIMES_COMMAND} must be < {i+1}-th of {END_DATETIMES_COMMAND}!")
                    if(self.isStrictParsing):
                        return False
                    continue

                elif(currentEndDatetime >= currentFutureDatetime):
                    print(f"Error. In {symbol} - {i+1}-th of {END_DATETIMES_COMMAND} must be < {i+1}-th of {FUTURE_DATETIMES_COMMAND}!")
                    if(self.isStrictParsing):
                        return False
                    continue

                elif(currentTimeInterval[1] == -1):
                    print(f"Error. In {symbol} - {i+1}-th time interval must be valid format!")
                    if(self.isStrictParsing):
                        return False
                    continue

                validStartDatetimes.append(currentStartDatetime)
                validEndDatetimes.append(currentEndDatetime)
                validFutureDatetimes.append(currentFutureDatetime)
                validTimeIntervals.append(currentTimeInterval)

            if(len(validStartDatetimes)*len(validEndDatetimes)*len(validTimeIntervals)*len(validTimeIntervals) == 0):
                print(f"Error. In {symbol} - have not valid values in field!")
                return False
            else:
                self.cryptocurrencies.append(CryptocurrencyInformation(symbol, validStartDatetimes, validEndDatetimes, validFutureDatetimes, validTimeIntervals))
                return True

        else:
            print(f"Error. In {symbol} - Not valid lengths: len({START_DATETIMES_COMMAND}) != len({END_DATETIMES_COMMAND}) != len({FUTURE_DATETIMES_COMMAND}) != len({TIME_INTERVALS_COMMAND}) -> {startDatetimesLen} != {endDatetimesLen} != {futureDatetimesLen} != {timeIntervalsLen}!")
            return False

    def __getJsonContentOf(self, fileName: str) -> dict[str, Any]:
        with open(fileName, "r", encoding="utf-8") as file:
            data = jsonLoad(file)

        return data
    
class PredictedPricePrinter:
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
            cryptocurrency.timeIntervals, range(0, len(cryptocurrency.startDatetimes))
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

            if(i % 4 == 0):
                sleep(2)

        print("=================================================================")
        sleep(2)

    def __printDatetimeInformation(self, datetimeInterval: tuple[datetime, datetime], timeInterval: str):
        print("Datetime interval:")
        print(f"From {datetimeInterval[0].strftime(STR_DATE_FORMAT)} to {datetimeInterval[1].strftime(STR_DATE_FORMAT)}")
        print(f"Time interval: {timeInterval}")

    def __printInformationAboutFuturePrice(self, startInformation: str, futurePrice: tuple[int, float], pastPrice: tuple[int, float]):
        print(startInformation)
        
        pastDatetime: str = datetime.fromtimestamp(pastPrice[0]/1000).strftime(STR_DATE_FORMAT)
        futureDatetime: str = datetime.fromtimestamp(futurePrice[0]/1000).strftime(STR_DATE_FORMAT)

        print(f"Price from {pastPrice[1]}({pastDatetime}) move to {futurePrice[1]}({futureDatetime})")
        print(f"The relative change is: {(futurePrice[1] - pastPrice[1])/futurePrice[1]*100}%")