from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.dirname(osPath.abspath(__file__))))
sysPath.append(rootDirectory)

from predictionalgorithm import *
from random import uniform
from random import randint
from datetime import (datetime, timedelta)
from priceparser import *
import graphic

STR_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

def drawImportanceCoefficientOf(symbol: str):
    cryptocurrenctParser: PriceParserBinanceAPI = PriceParserBinanceAPI(symbol)
    cryptocurrenctParser.timeInterval = "2h"
    cryptocurrenctParser.priceCount = 42*2 + 1

    endTime: datetime = datetime.now() - timedelta(days=1)
    startTime: datetime = endTime - timedelta(days=7)
    sourcePrices: list[PriceInformation] = cryptocurrenctParser.getPricesByProperties(startTime, endTime)

    openPrices, closePrices = getXYFormatFrom(sourcePrices)
    
    openPs: list[tuple[int, float]] = generateAllImportanceCoefficients(openPrices)
    closePs: list[tuple[int, float]] = generateAllImportanceCoefficients(closePrices)

    ps: list[PriceInformation] = []
    for op, cl in zip(openPs, closePs):
        ps.append(PriceInformation(datetime.fromtimestamp(op[0]//1000), op[1], cl[1]))

    graphic.drawPriceGraphics(ps)

    graphic.setTitleName(f"{symbol} importance coefficients")
    graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
    graphic.setYLabel("Importance coefficient")

    graphic.setDateFormat(STR_DATE_FORMAT)
    graphic.setPriceFormat()

    graphic.showLegend()
    graphic.show()

def drawPredictionPricesOf(symbol: str):
    cryptocurrenctParser: PriceParserBinanceAPI = PriceParserBinanceAPI(symbol)
    cryptocurrenctParser.timeInterval = "30m"
    cryptocurrenctParser.priceCount = 336 + 1

    endTime: datetime = datetime.now() - timedelta(days=0)
    startTime: datetime = endTime - timedelta(days=7)
    sourcePrices: list[PriceInformation] = cryptocurrenctParser.getPricesByProperties(startTime, endTime)

    openPrices, closePrices = getXYFormatFrom(sourcePrices)

    futureTime: int = int((endTime + timedelta(hours=11)).timestamp()*1000)
    futureOpenPrices = getPredictedFuturePricesIn(openPrices, futureTime)
    futureClosePrices = getPredictedFuturePricesIn(closePrices, futureTime)

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

    graphic.setTitleName(f"{symbol} predict vizualization")
    graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
    graphic.setYLabel("Price, $")

    graphic.setDateFormat(STR_DATE_FORMAT)
    graphic.setPriceFormat()

    graphic.showLegend()
    graphic.show()

def drawPredictionPriceWithRandomValues(minY: float, maxY: float):
    length: int = randint(100, 150)
    pastX: datetime = datetime.now() - timedelta(hours=length+2)
    datetimes: list[datetime] = []
    prices: list[float] = []
    generatedGraphic: list[tuple[int, float]] = []
    
    y: float = 0.0

    for i in range(0, length):
        y = uniform(minY, maxY)

        datetimes.append(pastX + timedelta(hours=1))
        prices.append(y)

        generatedGraphic.append((int(datetimes[-1].timestamp()*1000), prices[-1]))

        pastX += timedelta(hours=1)

    futurePrices: list[tuple[int, float]] = getPredictedFuturePricesIn(generatedGraphic, int(datetime.now().timestamp()*1000))

    graphic.drawLiniearGraphic(datetimes, prices, "green", "Source prices")
    futureDatetimes: list = [datetime.fromtimestamp(x[0]//1000) for x in futurePrices]
    futureDatetimes.insert(0, datetimes[-1])

    futurePriceValues: list[float] = [x[1] for x in futurePrices]
    futurePriceValues.insert(0, prices[-1])

    graphic.drawLiniearGraphic(futureDatetimes, futurePriceValues, "orange", "Future prices")

    graphic.setTitleName(f"Predict vizualization with random data")
    graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
    graphic.setYLabel("Price, $")

    graphic.setDateFormat(STR_DATE_FORMAT)
    graphic.setPriceFormat()

    graphic.showLegend()
    graphic.show()