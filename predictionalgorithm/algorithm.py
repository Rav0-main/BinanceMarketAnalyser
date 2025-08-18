from .graphichandler import IterationDataHandlerOfGraphic
from .pricepredicter import PricePredicter
from math import ceil
from math import log as ln

def generateAllImportanceCoefficients(marketGraphic: list[tuple[int, float]]) -> list[tuple[int, float]]:
    """
    TIME COMPLEXITY: O(3*n) ~ O(n), n = len(marketGraphic)\n
    MEMORY COMPLEXITY: O(n+k+m) ~(average) O(n), k = len(biggest_monotonic_sequence), m = count upping and downing sequence\n

    1) * marketGraphic[i][0] - timestamp in ms\n
       * marketGraphic[i][1] - price value\n
    """
    priceIterator = map(lambda x: x[1], marketGraphic)
    maxPrice: float = max(priceIterator)
    
    priceIterator = map(lambda x: x[1], marketGraphic)
    minPrice: float = min(priceIterator)
    
    marketGraphicAnalyser: IterationDataHandlerOfGraphic = IterationDataHandlerOfGraphic(
        (marketGraphic[0][0], marketGraphic[-1][0]),
        (minPrice, maxPrice)
    )

    pResults: list[tuple[int, float]] = []
    marketGraphicAnalyser.currentMonotonicSequence.append(marketGraphic[0][1])
    
    for timestamp, price in marketGraphic[1:]:
        p: tuple[float, int] = marketGraphicAnalyser(timestamp, price)
        pResults.append((timestamp, p[0]))
    
    return pResults

def getPredictedFuturePricesIn(marketGraphic: list[tuple[int, float]], futureTime: int) -> list[tuple[int, float]]:
    """
    TIME COMPLEXITY: O(3 * (2*n + k)/2 * (k+1)) ~ O(n*k), n = len(marketGraphic), k = count prices to predict\n
    MEMORY COMPLEXITY: O(k+m), k = len(biggest_monotonic_sequence), m = count upping and downing sequence

    1) * marketGraphic[i][0] - timestamp in ms\n
       * marketGraphic[i][1] - price value\n
    2) * futureTime - timestamp in ms > marketGraphic[-1][0]\n
    3) * changes a marketGraphic for adding future prices\n
    """
    
    futurePricesByTime: list[tuple[int, float]] = []
    avgDeltaTime: int = ceil((marketGraphic[-1][0] - marketGraphic[0][0]) / len(marketGraphic))

    while(marketGraphic[-1][0] < futureTime):
        onlyPriceValues = [x[1] for x in marketGraphic]
        maximumPrice: float = max(onlyPriceValues)
        mininumPrice: float = min(onlyPriceValues)
    
        marketGraphicAnalyser: IterationDataHandlerOfGraphic = IterationDataHandlerOfGraphic(
            (marketGraphic[0][0], marketGraphic[-1][0]),
            (mininumPrice, maximumPrice)
        )

        pastPrice: float = marketGraphic[0][1]
        pastTimestamp: float = marketGraphic[0][0]

        avgDeltaTime: int = ceil((marketGraphic[-1][0] - marketGraphic[0][0]) / (len(marketGraphic)-1))
        avgDeltaTime: int = min(avgDeltaTime, futureTime-marketGraphic[-1][0])

        pointAnalyse: tuple[float, int] = (0, 0)
        
        upKavg: float = 0
        downKavg: float = 0

        pricePredicter: PricePredicter = PricePredicter(
            avgDeltaTime, marketGraphic[-1][1], marketGraphicAnalyser,
            ln(maximumPrice / mininumPrice), ln(maximumPrice / mininumPrice)
        )

        for timestamp, price in marketGraphic[1:]:
            pointAnalyse = marketGraphicAnalyser(timestamp, price)

            upKavg += pointAnalyse[0] * (price - pastPrice)
            downKavg += pointAnalyse[0] * (timestamp - pastTimestamp)

            pastPrice = price
            pastTimestamp = timestamp

        kAvg: float = upKavg / downKavg
        
        futurePrice: float = pricePredicter.getPredictBy(kAvg, pointAnalyse)

        marketGraphic.append((marketGraphic[-1][0] + avgDeltaTime, futurePrice))
        futurePricesByTime.append(marketGraphic[-1])

    return futurePricesByTime