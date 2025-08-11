from math import log as ln
from math import exp
from math import ceil

class ImportanceCoefficientGenerator:
    p0: float
    k: float
    alpha: float
    Xn: float
    X0: float

    def __init__(self, timestampDiaposon: tuple[int, int], priceDiaposon: tuple[float, float]):
        """
        1) * timestampDiaposon[0] - min{timestamps}
           * timestampDiaposon[1] - max{timestamps}
        2) * priceDiaposon[0] - min{priceValues}
           * priceDiaposon[1] - max{priceValues}
        """
        self.k = priceDiaposon[0]/priceDiaposon[1]
        self.p0 = self.k*timestampDiaposon[0]/timestampDiaposon[1]
        self.alpha = exp((1-self.p0)/self.k)
        self.Xn = timestampDiaposon[1]
        self.X0 = timestampDiaposon[0]

    def getResult(self, timestamp: int):
        upLn: float = timestamp - self.Xn - self.alpha * (timestamp - self.X0)
        downLn: float = self.alpha * (self.X0 - self.Xn)
        lnRes: float = ln(upLn/downLn)
        return 1 + self.k * lnRes
    
    def __call__(self, timestamp: int) -> float:
        return self.getResult(timestamp)
    
def generateAllImportanceCoefficients(marketGraphic: list[tuple[int, float]]) -> list[tuple[int, float]]:
    priceIterator = map(lambda x: x[1], marketGraphic)
    maxPrice: float = max(priceIterator)
    
    priceIterator = map(lambda x: x[1], marketGraphic)
    minPrice: float = min(priceIterator)
    
    Pi: ImportanceCoefficientGenerator = ImportanceCoefficientGenerator(
        (marketGraphic[0][0], marketGraphic[-1][0]),
        (minPrice, maxPrice)
    )

    pResults: list[tuple[int, float]] = []
    for timestamp, price in marketGraphic[1:]:
        pResults.append((timestamp, Pi(timestamp)))

    return pResults

def getPredictedFuturePricesIn(marketGraphic: list[tuple[int, float]], futureTime: int) -> list[tuple[int, float]]:
    """
    1) * marketGraphic[i][0] - timestamp in ms
       * marketGraphic[i][1] - price value
    2) * futureTime - timestamp in ms > marketGraphic[-1][0]
    """
    
    futurePricesByTime: list[tuple[int, float]] = []
    avgDeltaTime: int = ceil((marketGraphic[-1][0] - marketGraphic[0][0]) / len(marketGraphic))

    while(avgDeltaTime + marketGraphic[-1][0] < futureTime):
        onlyPriceValues = [x[1] for x in marketGraphic]
        maxPrice: float = max(onlyPriceValues)
        minPrice: float = min(onlyPriceValues)
    
        Pi: ImportanceCoefficientGenerator = ImportanceCoefficientGenerator(
            (marketGraphic[0][0], marketGraphic[-1][0]),
            (minPrice, maxPrice)
        )

        pastPrice: float = marketGraphic[0][1]
        pastTimestamp: float = marketGraphic[0][0]
        avgDeltaTime: int = ceil((marketGraphic[-1][0] - marketGraphic[0][0]) / len(marketGraphic))
        p: float = 0
        upKavg: float = 0
        downKavg: float = 0

        for timestamp, price in marketGraphic[1:]:
            p = Pi(timestamp)
            upKavg += p * (price - pastPrice)
            downKavg += p * (timestamp - pastTimestamp)

            pastPrice = price
            pastTimestamp = timestamp

        kResult: float = upKavg / downKavg
        futurePrice: float = kResult * avgDeltaTime + marketGraphic[-1][1]
        marketGraphic.append((avgDeltaTime + marketGraphic[-1][0], futurePrice))
        futurePricesByTime.append(marketGraphic[-1])

    return futurePricesByTime