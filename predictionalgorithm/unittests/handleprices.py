from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.dirname(osPath.dirname(osPath.abspath(__file__))))
sysPath.append(rootDirectory)

from modellingparameters import *
from predictionalgorithm import *
from priceparser import *
from time import sleep

STR_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

def handlePricesOf(cryptocurrencies: list[str], parameters: ParametersToModellingInterface):
    """
    1) Price to predict is last price from parsing
    """

    print(parameters.modellingName)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    cryptocurrencyParser: PriceParserBinanceAPI = PriceParserBinanceAPI("NULL")
    WAIT_TIME: float = 1.5

    deltaPricePredictedCount: int = 0
    testcaseCount: int = len(cryptocurrencies)*len(parameters.parsingDatetimes)
    precentOfDeltaOpenPrices: list[float] = []
    precentOfDeltaClosePrices: list[float] = []

    for cryptocurrency in cryptocurrencies:
        cryptocurrencyParser.cryptocurrencySymbol = cryptocurrency

        print(f"CURRENT CRYPTO CURRENCY: {cryptocurrency}")
        print("==============================================================")

        for time, timeInterval, priceCount, endTimeOfInput, i in \
            zip(parameters.parsingDatetimes,
                parameters.timeIntervalsBetweenPrices,
                parameters.priceCounts,
                parameters.endDatetimesToModellingPredict,
                range(1, len(parameters.parsingDatetimes)+1)):
            
            cryptocurrencyParser.priceCount = priceCount
            cryptocurrencyParser.timeInterval = timeInterval
            parsedPrices: list[PriceInformation] = cryptocurrencyParser.getPricesByProperties(time[0], time[1])

            priceToPredict: PriceInformation = PriceInformation(parsedPrices[-1].time, parsedPrices[-1].open, parsedPrices[-1].close)

            parsedPrices: list[PriceInformation] = [x for x in parsedPrices if (x.time <= endTimeOfInput)]
            openPrices, closePrices = getXYFormatFrom(parsedPrices)
            
            openFuturePrices = getPredictedFuturePricesIn(openPrices, int(priceToPredict.time.timestamp()*1000))
            closeFuturePrices = getPredictedFuturePricesIn(closePrices, int(priceToPredict.time.timestamp()*1000))

            predictedOpenPriceValue: float = openFuturePrices[-1][1]
            predictedOpenPriceDatetime: datetime = datetime.fromtimestamp(openFuturePrices[-1][0]/1000)
            
            predictedClosePriceValue: float = closeFuturePrices[-1][1]
            predictedClosePriceDatetime: datetime = datetime.fromtimestamp(closeFuturePrices[-1][0]/1000)

            print(f"case №{i}:")
            print(f"* parsing datetime moment: {time[0].strftime(STR_DATE_FORMAT)}-{parsedPrices[-1].time.strftime(STR_DATE_FORMAT)}")
            print(f"* time interval: {timeInterval}")

            print("-------------------------------------")

            print(f"* truth open price: {priceToPredict.open}$, datetime: {priceToPredict.time.strftime(STR_DATE_FORMAT)}")
            print(f"* predicted open price: {predictedOpenPriceValue}$, datetime: {predictedOpenPriceDatetime.strftime(STR_DATE_FORMAT)}")

            precentOfDeltaOpenPrices.append((priceToPredict.open-predictedOpenPriceValue)/priceToPredict.open * 100)
            print(f"* precent difference: {precentOfDeltaOpenPrices[-1]}%")
            
            if(printDeltaPriceResult(priceToPredict.open, predictedOpenPriceValue, parsedPrices[-1].open)):
                deltaPricePredictedCount += 1

            print("-------------------------------------")

            print(f"* truth close price: {priceToPredict.close}$, datetime: {priceToPredict.time.strftime(STR_DATE_FORMAT)}")
            print(f"* predicted close price: {predictedClosePriceValue}$, datetime: {predictedClosePriceDatetime.strftime(STR_DATE_FORMAT)}")

            precentOfDeltaClosePrices.append((priceToPredict.close-predictedClosePriceValue)/priceToPredict.close * 100)
            print(f"* precent difference: {precentOfDeltaClosePrices[-1]}%")

            if(printDeltaPriceResult(priceToPredict.close, predictedClosePriceValue, parsedPrices[-1].close)):
                deltaPricePredictedCount += 1

            print()

            sleep(WAIT_TIME)
    
    precentOfDeltaOpenPrices.sort()
    precentOfDeltaClosePrices.sort()

    print("==============================================================")

    print()
    print("TEST RESULT:")
    print(f"* all test count(with open and close prices): {testcaseCount*2}")
    print(f"* delta price(open and close) truth predicted count: {deltaPricePredictedCount}")
    print(f"* precent of test count with true predicted delta prices: {deltaPricePredictedCount/(testcaseCount*2)*100}%")
    
    print()

    print(f"* median predictioned precent of open prices: {precentOfDeltaOpenPrices[testcaseCount//2]}%")
    print(f"* median predictioned precent of close prices: {precentOfDeltaClosePrices[testcaseCount//2]}%")

    print()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    print()

def printDeltaPriceResult(sourcePrice: float, predictedPrice: float, pastPrice: float) -> bool:
    """
    Returns sign(real_delta_price) == sign(predicted_delta_price)
    """

    realDeltaPrice: float = sourcePrice - pastPrice
    predictedDeltaPrice: float = predictedPrice - pastPrice
    print(f"* measuring direction from price: {pastPrice}$")

    if(realDeltaPrice*predictedDeltaPrice >= 0):
        print(f"* TRUTH. Delta price predicted!")
        return True
    else:
        print(f"* MISTAKE. Delta price not predicted!")
        return False