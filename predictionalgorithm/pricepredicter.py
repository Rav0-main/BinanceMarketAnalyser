from .graphichandler import IterationDataHandlerOfGraphic
from math import exp

class NotValidPointTypeException(Exception):
    pass

class PriceValuePredicter:
    __deltaTime: int
    __lastPrice: float
    __analyser: IterationDataHandlerOfGraphic
    __localMaximumCoefficient: float
    __localMinimumCoefficient: float

    def __init__(self, deltaTimeBetweenLastAndFuturePrices: int,
                 lastPrice: float, graphicAnalyser: IterationDataHandlerOfGraphic,
                 toLocalMaximumCoefficient: float, toLocalMinimumCoefficient: float):
        self.__deltaTime = deltaTimeBetweenLastAndFuturePrices
        self.__lastPrice = lastPrice
        self.__analyser = graphicAnalyser
        self.__localMaximumCoefficient = toLocalMaximumCoefficient
        self.__localMinimumCoefficient = toLocalMinimumCoefficient

    def getPredictBy(self, averageLineCoefficient: float, pointAnalyse: tuple[float, int]):
        kAvg: float = averageLineCoefficient
        firstPredict: float = kAvg * self.__deltaTime + self.__lastPrice

        if(pointAnalyse[1] == 0):
            return firstPredict
        
        secondPredict: float = (self.__lastPrice + 
        (self.__analyser.DMSEdgeCount * self.__analyser.medianDeltaPriceOfUMS
        - self.__analyser.UMSEdgeCount * self.__analyser.medianDeltaPriceOfDMS)/
        (self.__analyser.UMSEdgeCount + self.__analyser.DMSEdgeCount))

        if(pointAnalyse[1] == 1):
            probability = self.__getProbabilityOfSetNewLocalMaximumPrice()
            
            if(probability < 0.5 and secondPredict >= self.__lastPrice):
                return secondPredict
            elif(probability < 0.5 and secondPredict < self.__lastPrice):
                return (3 * secondPredict - self.__lastPrice) / self.__lastPrice
            elif(secondPredict >= self.__lastPrice):
                return 2*self.__lastPrice - secondPredict
            else:
                return secondPredict
            
        elif(pointAnalyse[1] == -1):
            probability = self.__getProbabilityOfSetNewLocalMinimumPrice()
            
            if(probability < 0.5 and secondPredict >= self.__lastPrice):
                return (secondPredict + self.__lastPrice) / 2
            elif(probability < 0.5 and secondPredict < self.__lastPrice):
                return secondPredict
            elif(secondPredict >= self.__lastPrice):
                return secondPredict
            else:
                return (secondPredict + self.__lastPrice) / 2
            
        raise NotValidPointTypeException("Point type must be -1(DMS), 0(simple), 1(UMS)!")
    
    def __getProbabilityOfSetNewLocalMaximumPrice(self):
        first: float = exp(len(self.__analyser.currentMonotonicSequence))
        second: float = len(self.__analyser.localMaximumPrices) / (len(self.__analyser.localMaximumPrices) + len(self.__analyser.localMinimumPrices))
        M = self.__analyser.localMaximumPrices[-1]
        third: float = exp(-M[0] * (M[1] - self.__lastPrice) / M[1])

        return self.__localMaximumCoefficient * first * second * third
    
    def __getProbabilityOfSetNewLocalMinimumPrice(self):
        first: float = exp(1/len(self.__analyser.currentMonotonicSequence))
        second: float = len(self.__analyser.localMinimumPrices) / (len(self.__analyser.localMaximumPrices) + len(self.__analyser.localMinimumPrices))
        m = self.__analyser.localMinimumPrices[len(self.__analyser.localMinimumPrices)//2]
        third: float = exp(m[0] * (m[1] - self.__lastPrice)/m[1])

        return self.__localMinimumCoefficient * first * second * third