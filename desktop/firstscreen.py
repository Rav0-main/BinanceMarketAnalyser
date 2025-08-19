from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from .executor import ScreenExecutor
from .datetimeparser import (getDatetimeFrom,
                             getTimeIntervalFrom)
from .cryptocurrencychecker import cryptocurrencyExistsOnMarket
from .general import (TimeIntervalValidDiapasons,
                      STR_DATE_FORMAT)
from priceparser import (PriceParserBinanceAPI,
                         PriceInformation,
                         getXYFormatFrom)
from datetime import datetime
from predictionalgorithm import getPredictedFuturePricesIn
import graphic

class FirstScreenExecutor(ScreenExecutor):
    """
    The first screen's executor requests the necessary information - the start date, the end date, the future date, the interval, and displays a price graph over time.
    """

    __cryptocurrency: str
    __startDatetime: datetime
    __endDatetime: datetime
    __futureDatetime: datetime
    __timeInterval: str
    __timeIntervalInMs: int

    def __init__(self):
        pass

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

        print("Enter dates in the format yyyy-mm-dd.")
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

        futureDatetime: int = int(self.__futureDatetime.timestamp()*1000)
        futureOpenPrices = getPredictedFuturePricesIn(openPrices, futureDatetime)
        futureClosePrices = getPredictedFuturePricesIn(closePrices, futureDatetime)

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