from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.abspath(__file__)))
sysPath.append(rootDirectory)

from priceparser import *
from datetime import (datetime,
                      timedelta)

def cryptocurrencyExistsOnMarket(cryptocurrencySymbol: str) -> bool:
    cryptocurrencyParser = PriceParserBinanceAPI(cryptocurrencySymbol)
    startDatetime: datetime = datetime.now()-timedelta(hours=1)
    endDatetime: datetime = datetime.now()
    cryptocurrencyParser.timeInterval = "30m"
    cryptocurrencyParser.priceCount = 2
    
    try:
        cryptocurrencyParser.getPricesByProperties(startDatetime, endDatetime)
        return True
    except:
        return False
