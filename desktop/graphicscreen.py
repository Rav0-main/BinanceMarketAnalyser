from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from .executor import ScreenExecutor
from .datetimeparser import (getDatetimeFrom,
                             getTimeIntervalFrom)
from .cryptocurrencychecker import cryptocurrencyExistsOnMarket
from .general import (TimeIntervalValidDiapasons,
                      STR_DATE_FORMAT,
                      LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC)
from priceparser import (PriceParserBinanceAPI,
                         PriceInformation,
                         getXYFormatFrom)
from datetime import datetime
from predictionalgorithm import getPredictedFuturePricesIn
import graphic
from os import system

class ScreenExecutorWithGraphic(ScreenExecutor):
    """
    The first screen's executor requests the necessary information - the start date, the end date, the future date, the interval, and displays a price graph over time.
    """

    __cryptocurrency: str
    __startDatetime: datetime
    __endDatetime: datetime
    __futureDatetime: datetime
    __timeInterval: str
    __timeIntervalInMs: int
    _logging: bool

    def __init__(self, logging: bool):
        self._logging = logging

    def execute(self) -> bool:
        self.__inputCryptocurrencyAndDatetimes()
        print("Graphic launching...")
        self.__showGraphicWithPredictedPrices()
        return False

    def __inputCryptocurrencyAndDatetimes(self):
        run: bool = True

        print("Input the cryptocurrency symbol:", end=" ")
        while(run):
            self.__cryptocurrency: str = input()
            if(cryptocurrencyExistsOnMarket(self.__cryptocurrency)):
                run = False
            else:
                print("Error. You have probably entered the wrong currency or are not connected to the internet.")
                print("Try again:", end=" ")

        print("Enter dates.")
        run = True
        while(run):
            print("Start date:", end=" ")
            try:
                self.__startDatetime: datetime = getDatetimeFrom(input())
                run = False
            except ValueError:
                print("Error. Not valid format!")
                print("Try again.")

        run = True
        while(run):
            print("End date:", end=" ")
            try:
                self.__endDatetime: datetime = getDatetimeFrom(input())

                if(self.__startDatetime < self.__endDatetime):
                    run = False
                else:
                    print("Error. The start date must be earlier than the end date!")
                    print("Try again.")

            except ValueError:
                print("Error. Not valid format!")
                print("Try again.")

        run = True
        while(run):
            print("Future date:", end=" ")
            try:
                self.__futureDatetime: datetime = getDatetimeFrom(input())

                if(self.__endDatetime < self.__futureDatetime):
                    run = False
                else:
                    print("Error. The end date must be earlier than the future date!")
                    print("Try again.")
                    
            except ValueError:
                print("Error. Not valid format!")
                print("Try again.")

        print("Input time interval, for example 5m, 1h, 1d and etc:", end=" ")
        run = True
        while(run):
            self.__timeInterval = input()

            timeIntervalParsingResult: tuple[str, int] = getTimeIntervalFrom(self.__timeInterval,
                                                                             minutes=TimeIntervalValidDiapasons.minutes,
                                                                             hours=TimeIntervalValidDiapasons.hours,
                                                                             days=TimeIntervalValidDiapasons.days)

            if(timeIntervalParsingResult[0] == 'm'):
                print(f"Error. Format minutes is nm, where n biggers or equals {TimeIntervalValidDiapasons.minutes[0]} and less or equals {TimeIntervalValidDiapasons.minutes[1]}.")
                print("Try again:", end=" ")
            
            elif(timeIntervalParsingResult[0] == 'h'):
                print(f"Error. Format hours is nh, where n biggers or equals {TimeIntervalValidDiapasons.hours[0]} and less or equals {TimeIntervalValidDiapasons.hours[1]}.")
                print("Try again:", end=" ")
            
            elif(timeIntervalParsingResult[0] == 'd'):
                print(f"Error. Format days is nd, where n biggers or equals {TimeIntervalValidDiapasons.days[0]} and less or equals {TimeIntervalValidDiapasons.days[1]}.")
                print("Try again:", end=" ")
            
            elif(timeIntervalParsingResult[1] == -1):
                print("Error. Not valid format!")
                print("Try again:", end=" ")

            else:
                self.__timeIntervalInMs = timeIntervalParsingResult[1]
                run = False

    def __showGraphicWithPredictedPrices(self):
        cryptocurrencyParser = PriceParserBinanceAPI(self.__cryptocurrency)
        cryptocurrencyParser.timeInterval = self.__timeInterval
        cryptocurrencyParser.priceCount = int((self.__endDatetime.timestamp()-self.__startDatetime.timestamp())*1000)//self.__timeIntervalInMs

        sourcePrices: list[PriceInformation] = cryptocurrencyParser.getPricesByProperties(self.__startDatetime, self.__endDatetime)

        openPrices, closePrices = getXYFormatFrom(sourcePrices)
        lastOpenPrice: tuple[int, float] = openPrices[-1]
        lastClosePrice: tuple[int, float] = closePrices[-1]

        futureDatetime: int = int(self.__futureDatetime.timestamp()*1000)
        futureOpenPrices = getPredictedFuturePricesIn(openPrices, futureDatetime)
        futureClosePrices = getPredictedFuturePricesIn(closePrices, futureDatetime)

        if(self._logging):
            self.__logFutureOpenAndClosePrices((lastOpenPrice, futureOpenPrices[-1]), (lastClosePrice, futureClosePrices[-1]))

        graphic.drawPriceGraphics(sourcePrices)

        futureOpenDatetimes = [datetime.fromtimestamp(x[0]/1000) for x in futureOpenPrices]
        futureOpenDatetimes.insert(0, sourcePrices[-1].time)

        futureCloseDatetimes = [datetime.fromtimestamp(x[0]/1000) for x in futureClosePrices]
        futureCloseDatetimes.insert(0, sourcePrices[-1].time)

        futureOpenPriceValues = [x[1] for x in futureOpenPrices]
        futureOpenPriceValues.insert(0, sourcePrices[-1].open)

        futureClosePriceValues = [x[1] for x in futureClosePrices]
        futureClosePriceValues.insert(0, sourcePrices[-1].close)

        graphic.drawLiniearGraphic(futureOpenDatetimes, futureOpenPriceValues, "orange", "Predicted open prices")
        graphic.drawLiniearGraphic(futureCloseDatetimes, futureClosePriceValues, "purple", "Predicted close prices")

        graphic.setTitleName(f"{self.__cryptocurrency} prices by datetime")
        graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
        graphic.setYLabel("Price, $")

        graphic.setDateFormat(STR_DATE_FORMAT)
        graphic.setPriceFormat()

        graphic.showLegend()
        print("Graphic launched.")
        graphic.show()

    def __logFutureOpenAndClosePrices(self, openPriceInformation: tuple[tuple[int, float],tuple[int, float]], closePriceInformation: tuple[tuple[int, float], tuple[int, float]]):
        startLine: str = f"{self.__cryptocurrency} graphic log.\nDatetime moment: {datetime.now().strftime(STR_DATE_FORMAT)}.\nDatetime interval: {self.__startDatetime.strftime(STR_DATE_FORMAT)} - {self.__endDatetime.strftime(STR_DATE_FORMAT)}.\nTime interval: {self.__timeInterval}.\nPredict on datetime: {self.__futureDatetime.strftime(STR_DATE_FORMAT)}."
        dashLine: str = "-----------------------------------------------------------------"
        openPriceLine: str = f"1. Open Price:\nPrice from {openPriceInformation[0][1]:.3f}$ ({datetime.fromtimestamp(openPriceInformation[0][0] / 1000).strftime(STR_DATE_FORMAT)}) move to {openPriceInformation[1][1]:.3f}$ ({datetime.fromtimestamp(openPriceInformation[1][0] / 1000).strftime(STR_DATE_FORMAT)}).\nRelative precent: {(openPriceInformation[1][1] - openPriceInformation[0][1]) / openPriceInformation[0][1]*100:.3f}%."
        closePriceLine: str = f"2. Close Price:\nPrice from {closePriceInformation[0][1]:.3f}$ ({datetime.fromtimestamp(closePriceInformation[0][0] / 1000).strftime(STR_DATE_FORMAT)}) move to {closePriceInformation[1][1]:.3f}$ ({datetime.fromtimestamp(closePriceInformation[1][0] / 1000).strftime(STR_DATE_FORMAT)}).\nRelative precent: {(closePriceInformation[1][1] - closePriceInformation[0][1]) / closePriceInformation[0][1]*100:.3f}%."
        
        with open(LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC, "w") as logger:
            logger.write(startLine + "\n" + dashLine + "\n" + openPriceLine + "\n" + dashLine + "\n" + closePriceLine)

class FirstScreenExecutor(ScreenExecutorWithGraphic):
    _logging = False

    def __init__(self):
        pass

class SecondScreenExecutor(ScreenExecutorWithGraphic):
    _logging = True

    def __init__(self):
        pass

class FifthScreenExecutor(ScreenExecutor):
    def __init__(self):
        pass

    def execute(self) -> bool:
        system("cls")
        print("Screen requests data such as the start date, end date, future date, and time interval.\n\nBased on the provided data, it predicts the future price value and displays a graphic of price values on time.\n")
        print(" * 'start date' - is start date to parsing of price values.")
        print(" * 'end date' - is end date of parsing of price values.")
        print(" * 'future date' - is future date to predict.")
        print(" * 'time interval' - is time interval between price values in parsing data.")
        print()
        print("All dates must be in ISO format or relative format: 'now-ti' or 'now+ti' where ti - is time interval, for example now-30m, now-2h, now+1d")
        print()
        print("Time interval must be in format: 5m, 30m, 2h, 1d and etc.")
        print()
        print("Press <Enter> to continue")
        input()
        return False