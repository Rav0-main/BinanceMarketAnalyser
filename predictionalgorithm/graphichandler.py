from math import log as ln
from math import exp
from bisect import bisect_right

class IterationDataHandlerOfGraphic:
    __p0: float
    __k: float
    __Xn_1: float
    __X0: float
    __alpha: float
    __wasInDowning: bool
    __wasInUpping: bool
    __priceDeltiesInUpping: list[float]
    __priceDeltiesInDowning: list[float]

    currentMonotonicSequence: list[float]

    medianDeltaPriceInUpping: float
    medianDeltaPriceInDowning: float

    localMaximumPoints: list[tuple[float, float]]
    """
     * localMaximumPoints[i][0] - importance coefficient of point
     * localMaximumPoints[i][1] - price value of point
    """
    localMinimumPoints: list[tuple[float, float]]
    """
     * localMinimumPoints[i][0] - importance coefficient of point
     * localMinimumPoints[i][1] - price value of point
    """

    def __init__(self, timestampDiaposon: tuple[int, int], priceDiaposon: tuple[float, float]):
        """
        1) * timestampDiaposon[0] - min{timestamps}
           * timestampDiaposon[1] - max{timestamps}
        2) * priceDiaposon[0] - min{priceValues}
           * priceDiaposon[1] - max{priceValues}
        """
        self.__k = priceDiaposon[0]/priceDiaposon[1]
        self.__p0 = self.__k*timestampDiaposon[0]/timestampDiaposon[1]
        self.__alpha = exp((1-self.__p0)/self.__k)
        self.__Xn_1 = timestampDiaposon[1]
        self.__X0 = timestampDiaposon[0]

        self.currentMonotonicSequence: list[float] = []
        self.__wasInDowning: bool = False
        self.__wasInUpping: bool = False

        self.uppingCount: int = 0
        self.downingCount: int = 0

        self.__priceDeltiesInUpping: list[float] = []
        self.__priceDeltiesInDowning: list[float] = []

        """
        monotonic sequence of prices
        """

    def complete(self, timestamp: int, price: float) -> tuple[float, int]:
        """
        result[i][0] - p
        result[i][1] - 0, if simple point;
                       1, if point in upping sequence;
                       -1, if point downing sequence;
        """
        upLn: float = timestamp - self.__Xn_1 - self.__alpha * (timestamp - self.__X0)
        downLn: float = self.__alpha * (self.__X0 - self.__Xn_1)
        lnRes: float = ln(upLn/downLn)

        p: float = 1 + self.__k * lnRes

        if(len(self.currentMonotonicSequence) <= 1):
            self.currentMonotonicSequence.append(price)
            return (p, 0)

        elif(len(self.currentMonotonicSequence) == 2 and self.currentMonotonicSequence[0] <= self.currentMonotonicSequence[1] and self.currentMonotonicSequence[1] > price):
            self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
            return (p, 0)
        
        elif(len(self.currentMonotonicSequence) == 2 and self.currentMonotonicSequence[0] > self.currentMonotonicSequence[1] and self.currentMonotonicSequence[1] <= price):
            self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
            return (p, 0)

        elif(self.currentMonotonicSequence[-1] <= price and not self.__wasInDowning):
            self.currentMonotonicSequence.append(price)
            self.uppingCount += 1
            self.__wasInUpping = True
            self.__wasInDowning = False
            return (p, 1)

        elif(self.currentMonotonicSequence[-1] <= price and self.__wasInDowning):
            currentDeltaPrice: float = self.currentMonotonicSequence[0]-self.currentMonotonicSequence[-1]
            appendIndex: int = bisect_right(self.__priceDeltiesInDowning, currentDeltaPrice)
            self.__priceDeltiesInDowning.insert(appendIndex, currentDeltaPrice)
            self.medianDeltaPriceInDowning = self.__priceDeltiesInDowning[len(self.__priceDeltiesInDowning)//2]

            self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
            self.__wasInDowning = False
            self.__wasInUpping = False
            return (p, 0)

        elif(self.__wasInUpping):
            currentDeltaPrice: float = self.currentMonotonicSequence[-1]-self.currentMonotonicSequence[0]
            appendIndex: int = bisect_right(self.__priceDeltiesInUpping, currentDeltaPrice)
            self.__priceDeltiesInUpping.insert(appendIndex, currentDeltaPrice)
            self.medianDeltaPriceInUpping = self.__priceDeltiesInUpping[len(self.__priceDeltiesInUpping)//2]

            self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
            self.__wasInDowning = True
            self.__wasInUpping = False
            self.downingCount += 1
            return (p, -1)
        
        else:
            self.currentMonotonicSequence.append(price)
            self.__wasInDowning = True
            self.__wasInUpping = False
            self.downingCount += 1
            return (p, -1)
        
    def getImportanceCoefficient(self, timestamp: int) -> float:
        """
        timestamp - in ms
        """
        upLn: float = timestamp - self.__Xn_1 - self.__alpha * (timestamp - self.__X0)
        downLn: float = self.__alpha * (self.__X0 - self.__Xn_1)
        lnRes: float = ln(upLn/downLn)

        return 1 + self.__k * lnRes
    
    def __call__(self, timestamp: int, price: float) -> 'tuple[float, int]':
        return self.complete(timestamp, price)