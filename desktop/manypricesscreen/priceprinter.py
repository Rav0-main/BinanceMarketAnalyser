from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from .cryptocurrencyinformation import CryptocurrencyInformation
from cryptocurrencymanager import (CryptocurrencyManager,
                                   CryptocurrencyInputPredictProtocol)
from datetime import datetime
from general import (STR_DATE_FORMAT,
                     LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES,
                     FILE_NAME_WITH_CRYPTOCURRENCIES)
from time import sleep
from typing import TextIO

class PredictionPricesPrinter:
    __timeSleep: float = 2.0
    __sleepCycle: int = 4

    __firstDashLine: str = "================================================================="
    __secondDashLine: str = "-----------------------------------------------------------------"

    __loggingInformation: str = ""
    __loggingFile: TextIO

    def __init__(self, cryptocurrencyManager: CryptocurrencyManager):
        self.__cryptocurrencyManager = cryptocurrencyManager

    def printPredictionPricesOf(self, cryptocurrencies: list[CryptocurrencyInformation], logging: bool):
        if(len(cryptocurrencies) == 0):
            print("Error. Not valid cryptocurrencies!")
            return
        
        if(logging):
            self.__loggingFile = open(LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES, "w")
            loggingStart: str = f"{FILE_NAME_WITH_CRYPTOCURRENCIES} log.\nDatetime moment: {datetime.now().strftime(STR_DATE_FORMAT)}.\n{self.__firstDashLine}\n"
            self.__loggingFile.write(loggingStart)

        for cryptocurrency in cryptocurrencies:
            self.__printPredictionPricesOfOneCryptocurrency(cryptocurrency, logging)

        if(logging):
            self.__loggingFile.close()

    def __printPredictionPricesOfOneCryptocurrency(self, cryptocurrency: CryptocurrencyInformation, logging: bool):
        print(f"PREDICTION: {cryptocurrency.symbol}")
        print(self.__firstDashLine)

        self.__loggingInformation: str = f"PREDICTION: {cryptocurrency.symbol}.\n{self.__firstDashLine}\n"

        for startDatetime, endDatetime, futureDatetime, timeInterval, i in zip(cryptocurrency.startDatetimes,
            cryptocurrency.endDatetimes, cryptocurrency.futureDatetimes,
            cryptocurrency.timeIntervals, range(1, len(cryptocurrency.startDatetimes)+1)
            ):

            protocol = self.__cryptocurrencyManager.predict(
                CryptocurrencyInputPredictProtocol(
                    cryptocurrency.symbol, (startDatetime, endDatetime), timeInterval, 
                    futureDatetime
                )
            )

            if(i != 1):
                print(self.__secondDashLine)
                self.__loggingInformation = self.__loggingInformation + self.__secondDashLine + "\n"

            self.__printDatetimeInformation((startDatetime, endDatetime), timeInterval[0])
            print()

            startInformation: str = "1. Open Price"
            self.__loggingInformation = self.__loggingInformation + "1. Open Price:\n"
            self.__printInformationAboutPredictionPrice(startInformation,
            protocol.predictionOpenPricesInTimestamp[-1], protocol.lastParsedOpenPriceInTimestamp)

            print()

            startInformation = "2. Close Price"
            self.__loggingInformation = self.__loggingInformation + "2. Close Price:\n"
            self.__printInformationAboutPredictionPrice(startInformation,
            protocol.predictionClosePricesInTimestamp[-1], protocol.lastParsedClosePriceInTimestamp)
            
            print()
            
            if(i % self.__sleepCycle == 0):
                sleep(self.__timeSleep)

        print(self.__firstDashLine)
        self.__loggingInformation = self.__loggingInformation + self.__firstDashLine + "\n"
        
        if(logging):
            self.__loggingFile.write(self.__loggingInformation)
            
        self.__loggingInformation = ""

        sleep(self.__timeSleep)

    def __printDatetimeInformation(self, datetimeInterval: tuple[datetime, datetime], timeInterval: str):
        print("Datetime interval:")
        print(f"From {datetimeInterval[0].strftime(STR_DATE_FORMAT)} to {datetimeInterval[1].strftime(STR_DATE_FORMAT)}")
        print(f"Time interval: {timeInterval}")

        self.__loggingInformation = self.__loggingInformation + f"Datetime interval: {datetimeInterval[0].strftime(STR_DATE_FORMAT)} - {datetimeInterval[1].strftime(STR_DATE_FORMAT)}.\nTime interval: {timeInterval}.\n\n"

    def __printInformationAboutPredictionPrice(self, startInformation: str, predictionPrice: tuple[int, float], lastPrice: tuple[int, float]):
        print(startInformation)
        
        pastDatetime: str = datetime.fromtimestamp(lastPrice[0]/1000).strftime(STR_DATE_FORMAT)
        futureDatetime: str = datetime.fromtimestamp(predictionPrice[0]/1000).strftime(STR_DATE_FORMAT)

        print(f"Price from {lastPrice[1]:.3f}$ ({pastDatetime}) move to {predictionPrice[1]:.3f}$ ({futureDatetime})")
        print(f"Relative difference: {(predictionPrice[1] - lastPrice[1])/lastPrice[1]*100:.3f}%")

        self.__loggingInformation = self.__loggingInformation + f"Predict on datetime: {futureDatetime}.\n"
        self.__loggingInformation = self.__loggingInformation + f"Predict. Price from {lastPrice[1]:.3f}$ ({pastDatetime}) move to {predictionPrice[1]:.3f}$ ({futureDatetime}).\n" + f"Relative precent: {(predictionPrice[1] - lastPrice[1])/lastPrice[1]*100:.3f}%.\n\n"