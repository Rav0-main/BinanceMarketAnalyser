from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from .executor import ScreenExecutor
from .datetimeparser import *
from .cryptocurrencychecker import cryptocurrencyExistsOnMarket
from .general import (TimeIntervalValidDiapasons,
                      STR_DATE_FORMAT)
from priceparser import *
from datetime import datetime
from predictionalgorithm import *
import graphic

class FirstScreenExecutor(ScreenExecutor):
    cryptocurrency: str
    startDatetime: datetime
    endDatetime: datetime
    futureDatetime: datetime
    timeInterval: str
    timeIntervalInMs: int

    def __init__(self):
        pass

    def execute(self) -> bool:
        self.__inputCryptocurrencyAndDatetimes()
        self.__showGraphicWithPredictedPrices()
        return False

    def __inputCryptocurrencyAndDatetimes(self):
        run: bool = True

        print("Input the cryprocurrency symbol:")
        while(run):
            self.cryptocurrency: str = input()
            if(cryptocurrencyExistsOnMarket(self.cryptocurrency)):
                run = False
            else:
                print("Error. You have probably entered the wrong currency or are not connected to the internet.")

        print("Enter dates in the format yyyy-mm-dd.")
        run = True
        while(run):
            print("Start date:")
            try:
                self.startDatetime: datetime = getDatetimeFrom(input())
                run = False
            except ValueError:
                print("Error. You entered it incorrectly, need yyyy-mm-dd!")

        run = True
        while(run):
            print("End date:")
            try:
                self.endDatetime: datetime = getDatetimeFrom(input())

                if(self.startDatetime < self.endDatetime):
                    run = False
                else:
                    print("Error. The start date must be earlier than the end date!")

            except ValueError:
                print("Error. You entered it incorrectly, need yyyy-mm-dd!")

        run = True
        while(run):
            print("Future date:")
            try:
                self.futureDatetime: datetime = getDatetimeFrom(input())

                if(self.endDatetime < self.futureDatetime):
                    run = False
                else:
                    print("Error. The end date must be earlier than the future date!")
                    
            except ValueError:
                print("Error. You entered it incorrectly, need yyyy-mm-dd!")

        run = True
        while(run):
            print("Input time interval, for example 5m, 1h, 1d and etc.")
            self.timeInterval = input()

            timeIntervalParsingResult: tuple[str, int] = getTimeIntervalFrom(self.timeInterval,
                                                                             minutes=TimeIntervalValidDiapasons.minutes,
                                                                             hours=TimeIntervalValidDiapasons.hours,
                                                                             days=TimeIntervalValidDiapasons.days)

            if(timeIntervalParsingResult[0] == 'm'):
                print(f"Error. Format minutes is nm, where n biggers or equals {TimeIntervalValidDiapasons.minutes[0]} and less or equals {TimeIntervalValidDiapasons.minutes[1]}.")
            
            elif(timeIntervalParsingResult[0] == 'h'):
                print(f"Error. Format hours is nh, where n biggers or equals {TimeIntervalValidDiapasons.hours[0]} and less or equals {TimeIntervalValidDiapasons.hours[1]}.")

            elif(timeIntervalParsingResult[0] == 'd'):
                print(f"Error. Format days is nd, where n biggers or equals {TimeIntervalValidDiapasons.days[0]} and less or equals {TimeIntervalValidDiapasons.days[1]}.")

            elif(timeIntervalParsingResult[1] == -1):
                print("Error. Not valid format!")

            else:
                self.timeIntervalInMs = timeIntervalParsingResult[1]
                run = False

    def __showGraphicWithPredictedPrices(self):
        cryptocurrenctParser: PriceParserBinanceAPI = PriceParserBinanceAPI(self.cryptocurrency)
        cryptocurrenctParser.timeInterval = self.timeInterval
        cryptocurrenctParser.priceCount = int((self.endDatetime.timestamp()-self.startDatetime.timestamp())*1000)//self.timeIntervalInMs

        sourcePrices: list[PriceInformation] = cryptocurrenctParser.getPricesByProperties(self.startDatetime, self.endDatetime)

        openPrices, closePrices = getXYFormatFrom(sourcePrices)

        futureDatetime: int = int(self.futureDatetime.timestamp()*1000)
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

        graphic.setTitleName(f"{self.cryptocurrency} prices by datetime")
        graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
        graphic.setYLabel("Price, $")

        graphic.setDateFormat(STR_DATE_FORMAT)
        graphic.setPriceFormat()

        graphic.showLegend()
        graphic.show()