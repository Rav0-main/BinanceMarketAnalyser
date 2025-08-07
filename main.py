from priceparser import *
import graphic
from datetime import (datetime,
                      timedelta)

STR_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

CRYPTOCURRENCY_SYMBOL = "BTC"

bitcoinParser = PriceParserBinanceAPI(CRYPTOCURRENCY_SYMBOL)
bitcoinParser.priceCount = 48
bitcoinParser.timeInterval = "30m"

prices = bitcoinParser.getPricesByProperties(datetime.now()-timedelta(days=1), datetime.now())

graphic.drawPriceGraphics(prices)

graphic.setTitleName(f"{CRYPTOCURRENCY_SYMBOL} prices by datetime")
graphic.setXLabel(f"Datetime, format: {STR_DATE_FORMAT}")
graphic.setYLabel("Price, $")

graphic.setDateFormat(STR_DATE_FORMAT)
graphic.setPriceFormat()

graphic.showLegend()
graphic.show()