from math import log as ln
from math import exp
from bisect import bisect_right

class IterationDataHandlerOfGraphic:
    """
    Handle data stream of graphic, analys and save important information about graphic
     * Price values - axe Oy
     * Timestamps - axe Ox
     * Importance coefficient(aka p) - is a coefficient that shows how important the difference between the current price and the previous price is relative to the final price.
     
    Abbreviations:
     * UMS - upping monotonic sequence of price values (UMS[0] < UMS[1] < UMS[2] ...)
     * DMS - downing monotonic sequence of price values (DMS[0] > DMS[1] > DMS[2] ...)
     * Edge - is distance between two price values: sequence[i] <-> sequence[i+1], i = [0, len(sequence)-2] 
    """

    __p0: float
    __k: float
    __Xn_1: float
    __X0: float
    __alpha: float
    __wasInDMS: bool
    __wasInUMS: bool
    __priceDeltiesOfUMS: list[float]
    __priceDeltiesInDMS: list[float]
    __pastTimestamp: int

    localMaximumPrices: list[tuple[float, float]]
    """
    Sorted by localMaximumPrices[0][1] < localMaximumPrices[1][1] < localMaximumPrices[2][1] ...
     * localMaximumPoints[i][0] - importance coefficient
     * localMaximumPoints[i][1] - price value
    """

    localMinimumPrices: list[tuple[float, float]]
    """
    Sorted by localMinimumPrices[0][1] < localMinimumPrices[1][1] < localMinimumPrices[2][1] ...
     * localMinimumPoints[i][0] - importance coefficient
     * localMinimumPoints[i][1] - price value
    """

    currentMonotonicSequence: list[float]

    UMSEdgeCount: int
    """
    Edge count of upping monotonic sequence
    """
    DMSEdgeCount: int
    """
    Edge count of downing monotonic sequence
    """

    medianDeltaPriceOfUMS: float
    """
    Median delta price of all upping monotonic sequences in current moment(last given timestamp)
    """

    medianDeltaPriceOfDMS: float
    """
    Median delta price of all downing monotonic sequences in current moment(last given timestamp)
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

        self.__priceDeltiesOfUMS: list[float] = []
        self.__priceDeltiesInDMS: list[float] = []

        self.__wasInDMS: bool = False
        self.__wasInUMS: bool = False

        self.currentMonotonicSequence: list[float] = []

        self.UMSEdgeCount: int = 0
        self.DMSEdgeCount: int = 0

        self.medianDeltaPriceOfUMS: float = 0.0
        self.medianDeltaPriceOfDMS: float = 0.0

        self.localMaximumPrices: list[tuple[float, float]] = []
        self.localMinimumPrices: list[tuple[float, float]] = []

    def complete(self, timestamp: int, price: float) -> tuple[float, int]:
        """
        Handle of given point.\n
        Past given timestamp must be < timestamp for valid working.\n

        return_value[i][0] - importance coefficient
        return_value[i][1] - 0, if simple point;
                       1, if point in upping sequence;
                       -1, if point downing sequence;
        """
        p: float = self.getImportanceCoefficient(timestamp)
        returnValue: tuple[float, int] = (0, 0)

        if(len(self.currentMonotonicSequence) <= 1):
            self.currentMonotonicSequence.append(price)
            returnValue = (p, 0)

        elif(len(self.currentMonotonicSequence) == 2 and self.currentMonotonicSequence[0] <= self.currentMonotonicSequence[1] and self.currentMonotonicSequence[1] > price):
            self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
            returnValue = (p, 0)
        
        elif(len(self.currentMonotonicSequence) == 2 and self.currentMonotonicSequence[0] > self.currentMonotonicSequence[1] and self.currentMonotonicSequence[1] <= price):
            self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
            returnValue = (p, 0)

        elif(self.__isPointInUppingMonotonicSequence(price)):
            self.__handlePointInUppintMonotonicSequence(price)
            returnValue = (p, 1)

        elif(self.__isEndPointOfDowningMonotonicSequence(price)):
            self.__handleEndPointOfDowningMonotonicSequence(price)
            returnValue = (p, 0)

        elif(self.__wasInUMS):
            self.__handleEndPointOfUppingMonotonicSequence(price)
            returnValue = (p, -1)
        
        else:
            self.__handlePointInDowningMonotonicSequence(price)
            returnValue = (p, -1)
        
        self.__pastTimestamp = timestamp
        return returnValue
        
    def getImportanceCoefficient(self, timestamp: int) -> float:
        """
        timestamp - in ms
        """
        upLn: float = timestamp - self.__Xn_1 - self.__alpha * (timestamp - self.__X0)
        downLn: float = self.__alpha * (self.__X0 - self.__Xn_1)
        lnRes: float = ln(upLn/downLn)

        return 1 + self.__k * lnRes
    
    def __isPointInUppingMonotonicSequence(self, price: float) -> bool:
        return self.currentMonotonicSequence[-1] <= price and \
               not self.__wasInDMS
    
    def __handlePointInUppintMonotonicSequence(self, price: float):
        self.currentMonotonicSequence.append(price)
        self.UMSEdgeCount += 1
        self.__wasInUMS = True
        self.__wasInDMS = False

    def __isEndPointOfDowningMonotonicSequence(self, price: float) -> bool:
        return self.currentMonotonicSequence[-1] <= price and \
               self.__wasInDMS

    def __handleEndPointOfDowningMonotonicSequence(self, price: float):
        DMSDeltaPrice: float = self.currentMonotonicSequence[0]-self.currentMonotonicSequence[-1]
        appendIndex: int = bisect_right(self.__priceDeltiesInDMS, DMSDeltaPrice)
        self.__priceDeltiesInDMS.insert(appendIndex, DMSDeltaPrice)
        
        self.medianDeltaPriceOfDMS = self.__priceDeltiesInDMS[len(self.__priceDeltiesInDMS)//2]

        self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]

        appendIndex = bisect_right(self.localMinimumPrices, self.currentMonotonicSequence[0], key=lambda x: x[1])
        self.localMinimumPrices.insert(appendIndex, (self.getImportanceCoefficient(self.__pastTimestamp),
                                        self.currentMonotonicSequence[0]))
        
        self.__wasInDMS = False
        self.__wasInUMS = False

    def __handleEndPointOfUppingMonotonicSequence(self, price: float):
        UMSDeltaPrice: float = self.currentMonotonicSequence[-1]-self.currentMonotonicSequence[0]
        appendIndex: int = bisect_right(self.__priceDeltiesOfUMS, UMSDeltaPrice)
        self.__priceDeltiesOfUMS.insert(appendIndex, UMSDeltaPrice)
        self.medianDeltaPriceOfUMS = self.__priceDeltiesOfUMS[len(self.__priceDeltiesOfUMS)//2]

        self.currentMonotonicSequence = [self.currentMonotonicSequence.pop(), price]
        
        appendIndex = bisect_right(self.localMaximumPrices, self.currentMonotonicSequence[0], key=lambda x: x[1])
        self.localMaximumPrices.insert(appendIndex, (self.getImportanceCoefficient(self.__pastTimestamp),
                                        self.currentMonotonicSequence[0]))

        self.__wasInDMS = True
        self.__wasInUMS = False
        self.DMSEdgeCount += 1

    def __handlePointInDowningMonotonicSequence(self, price: float):
        self.currentMonotonicSequence.append(price)
        self.__wasInDMS = True
        self.__wasInUMS = False
        self.DMSEdgeCount += 1
    
    def __call__(self, timestamp: int, price: float) -> 'tuple[float, int]':
        """
        Calls a method 'complete' and returns it result 
        """
        return self.complete(timestamp, price)