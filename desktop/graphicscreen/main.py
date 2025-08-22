from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

rootDirectory = osPath.dirname(rootDirectory)
sysPath.append(rootDirectory)

from .datainputer import DataInputerOfGraphicScreen
from cryptocurrencymanager import (CryptocurrencyManager,
                                   CryptocurrencyInputPredictProtocol)
from executor import (ScreenExecutor,
                       ScreenOfLoggingOutputer)
from general import  (STR_DATE_FORMAT,
                      LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC)
from datetime import datetime
from os import system
import graphic

class ScreenExecutorWithGraphic(ScreenExecutor):
    """
    The graphic screen executor requests the necessary information - the start date, the end date, the future date, the interval, and displays a price graphic on time.
    """

    __cryptocurrencySymbol: str
    __startDatetime: datetime
    __endDatetime: datetime
    __futureDatetime: datetime
    __timeInterval: str
    __timeIntervalInMs: int
    __manager: CryptocurrencyManager
    _logging: bool

    def __init__(self, logging: bool):
        self._logging = logging
        self.__manager = CryptocurrencyManager()

    def execute(self) -> bool:
        system("cls")
        self.__inputGraphicData()

        print("Graphic launching...")

        self.__viewGraphicWithPredictionPrices()
        
        return False

    def __inputGraphicData(self):
        dataInputer = DataInputerOfGraphicScreen(self.__manager)
        dataInputer.input()

        self.__cryptocurrencySymbol = dataInputer.cryptocurrencySymbol
        self.__startDatetime = dataInputer.startDatetime
        self.__endDatetime = dataInputer.endDatetime
        self.__futureDatetime = dataInputer.futureDatetime
        self.__timeInterval = dataInputer.timeInterval
        self.__timeIntervalInMs = dataInputer.timeIntervalInMs

    def __viewGraphicWithPredictionPrices(self):
        protocol = self.__manager.predict(
            CryptocurrencyInputPredictProtocol(
                self.__cryptocurrencySymbol, (self.__startDatetime, self.__endDatetime),
                (self.__timeInterval, self.__timeIntervalInMs), self.__futureDatetime
            )
        )

        if(self._logging):
            self.__logFutureOpenAndClosePrices(
                (protocol.lastParsedOpenPriceInTimestamp, protocol.predictionOpenPricesInTimestamp[-1]),
                (protocol.lastParsedClosePriceInTimestamp, protocol.predictionClosePricesInTimestamp[-1])
            )

        graphic.drawPriceGraphics(protocol.parsedPrices)

        predictionOpenDatetimes = [datetime.fromtimestamp(x[0]/1000) for x in protocol.predictionOpenPricesInTimestamp]
        predictionOpenDatetimes.insert(0, protocol.parsedPrices[-1].datetime)

        predictionCloseDatetimes = [datetime.fromtimestamp(x[0]/1000) for x in protocol.predictionClosePricesInTimestamp]
        predictionCloseDatetimes.insert(0, protocol.parsedPrices[-1].datetime)

        predictionOpenPriceValues = [x[1] for x in protocol.predictionOpenPricesInTimestamp]
        predictionOpenPriceValues.insert(0, protocol.parsedPrices[-1].open)

        predictionClosePriceValues = [x[1] for x in protocol.predictionClosePricesInTimestamp]
        predictionClosePriceValues.insert(0, protocol.parsedPrices[-1].close)

        graphic.drawLiniearGraphic(predictionOpenDatetimes, predictionOpenPriceValues, "orange", "Predicted open prices")
        graphic.drawLiniearGraphic(predictionCloseDatetimes, predictionClosePriceValues, "purple", "Predicted close prices")

        graphic.setTitleName(f"{self.__cryptocurrencySymbol} prices by datetime")
        graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
        graphic.setYLabel("Price, $")

        graphic.setDateFormat(STR_DATE_FORMAT)
        graphic.setPriceFormat()

        graphic.showLegend()
        print("Graphic launched.")
        graphic.show()
        print("Graphic closed.")
        graphic.close()

    def __logFutureOpenAndClosePrices(self, openPriceInformation: tuple[tuple[int, float],tuple[int, float]], closePriceInformation: tuple[tuple[int, float], tuple[int, float]]):
        startLine: str = f"graphic log.\nPREDICTION: {self.__cryptocurrencySymbol}.\nDatetime moment: {datetime.now().strftime(STR_DATE_FORMAT)}.\nDatetime interval: {self.__startDatetime.strftime(STR_DATE_FORMAT)} - {self.__endDatetime.strftime(STR_DATE_FORMAT)}.\nTime interval: {self.__timeInterval}.\nPredict on datetime: {self.__futureDatetime.strftime(STR_DATE_FORMAT)}."
        dashLine: str = "-----------------------------------------------------------------"
        openPriceLine: str = f"1. Open Price:\nPredict. Price from {openPriceInformation[0][1]:.3f}$ ({datetime.fromtimestamp(openPriceInformation[0][0] / 1000).strftime(STR_DATE_FORMAT)}) move to {openPriceInformation[1][1]:.3f}$ ({datetime.fromtimestamp(openPriceInformation[1][0] / 1000).strftime(STR_DATE_FORMAT)}).\nRelative difference: {(openPriceInformation[1][1] - openPriceInformation[0][1]) / openPriceInformation[0][1]*100:.3f}%.\n"
        closePriceLine: str = f"2. Close Price:\nPredict. Price from {closePriceInformation[0][1]:.3f}$ ({datetime.fromtimestamp(closePriceInformation[0][0] / 1000).strftime(STR_DATE_FORMAT)}) move to {closePriceInformation[1][1]:.3f}$ ({datetime.fromtimestamp(closePriceInformation[1][0] / 1000).strftime(STR_DATE_FORMAT)}).\nRelative difference: {(closePriceInformation[1][1] - closePriceInformation[0][1]) / closePriceInformation[0][1]*100:.3f}%."
        
        with open(LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC, "w") as logger:
            logger.write(startLine + "\n" + dashLine + "\n" + openPriceLine + "\n" + closePriceLine)

class GraphicViewerScreenWithoutLogging(ScreenExecutorWithGraphic):
    _logging = False

    def __init__(self):
        super().__init__(self._logging)

class GraphicViewerScreenWithLogging(ScreenExecutorWithGraphic):
    _logging = True

    def __init__(self):
        super().__init__(self._logging)     

class LoggingOutputerOfGraphicViewerScreen(ScreenOfLoggingOutputer):
    def __init__(self):
        self._loggingFileName = LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC
        self._cryptocurrencyManager = CryptocurrencyManager()

class DocumentationScreenOfGraphicViewer(ScreenExecutor):
    def __init__(self):
        pass

    def execute(self) -> bool:
        system("cls")
        
        print("Screen requests data such as the start date, end date, future date and time interval.\n\nBased on the provided data, it predicts the future price value and displays a graphic of price values on time.\n")
        print(" * 'start date' - is start date to parsing of price values;")
        print(" * 'end date' - is end date of parsing of price values;")
        print(" * 'future date' - is future date to predict;")
        print(" * 'time interval' - is time interval between price values in parsing data.")
        print()
        print("All dates must be in ISO format or relative format: 'now-ti' or 'now+ti' where ti - is time interval, for example now-30m, now-2h, now+1d.")
        print()
        print("Time interval must be in format: 5m, 30m, 2h, 1d and etc.")
        print()
        
        print("Press <Enter> to continue")
        input()
        return False