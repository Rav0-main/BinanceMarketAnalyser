from priceparser import *
from datetime import (datetime,
                      timedelta)
from predictionalgorithm import getPredictedFuturePricesIn
import graphic

def handleCryptocurrency(symbol: str):
    cryptocurrenctParser: PriceParserBinanceAPI = PriceParserBinanceAPI(symbol)
    cryptocurrenctParser.timeInterval = "30m"
    cryptocurrenctParser.priceCount = 336 + 1

    endTime: datetime = datetime.now() - timedelta(days=0)
    startTime: datetime = endTime - timedelta(days=7)
    sourcePrices: list[PriceInformation] = cryptocurrenctParser.getPricesByProperties(startTime, endTime)

    openPrices, closePrices = getXYFormatFrom(sourcePrices)

    futureTime: int = int((endTime + timedelta(hours=24)).timestamp()*1000)
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

STR_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
CRYPTOCURRENCY_SYMBOL = "SOL"

handleCryptocurrency(CRYPTOCURRENCY_SYMBOL)

graphic.setTitleName(f"{CRYPTOCURRENCY_SYMBOL} prices by datetime")
graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
graphic.setYLabel("Price, $")

graphic.setDateFormat(STR_DATE_FORMAT)
graphic.setPriceFormat()

graphic.showLegend()
graphic.show()