from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

rootDirectory = osPath.dirname(rootDirectory)
sysPath.append(rootDirectory)

from .cryptocurrencyinformation import CryptocurrencyInformation
from .strcommands import *
from typing import Any
from general import (TimeIntervalValidDiapasons,
                     FILE_NAME_WITH_CRYPTOCURRENCIES)
from cryptocurrencychecker import cryptocurrencyExistsOnMarket
from datetimeparser import (getDatetimeFrom,
                            getTimeIntervalFrom)
from datetime import datetime
from json import load as jsonLoad

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