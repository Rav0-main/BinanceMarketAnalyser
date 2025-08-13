from .graphichandler import IterationDataHandlerOfGraphic
from math import ceil

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
    
    Pi: IterationDataHandlerOfGraphic = IterationDataHandlerOfGraphic(
        (marketGraphic[0][0], marketGraphic[-1][0]),
        (minPrice, maxPrice)
    )

    pResults: list[tuple[int, float]] = []
    Pi.currentMonotonicSequence.append(marketGraphic[0][1])
    
    for timestamp, price in marketGraphic[1:]:
        p: tuple[float, int] = Pi(timestamp, price)
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

    while(avgDeltaTime + marketGraphic[-1][0] < futureTime):
        onlyPriceValues = [x[1] for x in marketGraphic]
        maxPrice: float = max(onlyPriceValues)
        minPrice: float = min(onlyPriceValues)
    
        pGenerator: IterationDataHandlerOfGraphic = IterationDataHandlerOfGraphic(
            (marketGraphic[0][0], marketGraphic[-1][0]),
            (minPrice, maxPrice)
        )

        pastPrice: float = marketGraphic[0][1]
        pastTimestamp: float = marketGraphic[0][0]
        avgDeltaTime: int = ceil((marketGraphic[-1][0] - marketGraphic[0][0]) / len(marketGraphic))
        p: tuple[float, int] = (0, 0)
        upKavg: float = 0
        downKavg: float = 0

        for timestamp, price in marketGraphic[1:]:
            p = pGenerator(timestamp, price)
            upKavg += p[0] * (price - pastPrice)
            downKavg += p[0] * (timestamp - pastTimestamp)

            pastPrice = price
            pastTimestamp = timestamp

        kAvg: float = upKavg / downKavg
        futurePrice: float = kAvg * avgDeltaTime + marketGraphic[-1][1]

        if(p[1] == 0):
            pass
        else:
            secondFuturePrice: float = (pastPrice + 
            (pGenerator.downingCount * pGenerator.medianDeltaPriceInUpping - pGenerator.uppingCount * pGenerator.medianDeltaPriceInDowning)/(pGenerator.uppingCount + pGenerator.downingCount))

            futurePrice = (futurePrice + secondFuturePrice) / 2

        marketGraphic.append((avgDeltaTime + marketGraphic[-1][0], futurePrice))
        futurePricesByTime.append(marketGraphic[-1])

    return futurePricesByTime