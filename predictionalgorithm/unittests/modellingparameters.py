from datetime import (datetime, timedelta)
from abc import (ABC, abstractmethod)

CURRENT_TIME: datetime = datetime.now()

class ParametersToModellingInterface(ABC):
    modellingName: str

    parsingDatetimes: list[tuple[datetime, datetime]]
    """
     * parsingDatetimes[i][0] - start
     * parsingDatetimes[i][1] - end
     * parsingDatetimes[i][0] < parsingDatetimes[i][1] 
    """

    endDatetimesToModellingPredict: list[datetime]
    timeIntervalsBetweenPrices: list[str]
    priceCounts: list[int]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

class ParametersOnSmallDistances(ParametersToModellingInterface):
    modellingName: str = "HANDLE PRICES ON SMALL DISTANCE"

    parsingDatetimes: list[tuple[datetime, datetime]] = [
        (CURRENT_TIME-timedelta(days=2), CURRENT_TIME-timedelta(days=1) + timedelta(minutes=30)), 
        (CURRENT_TIME-timedelta(days=8), CURRENT_TIME-timedelta(days=1) + timedelta(hours=1)),
        (CURRENT_TIME-timedelta(days=32), CURRENT_TIME-timedelta(days=1) + timedelta(hours=4))
    ]

    endDatetimesToModellingPredict: list[datetime] = [
        CURRENT_TIME-timedelta(days=1),
        CURRENT_TIME-timedelta(days=1),
        CURRENT_TIME-timedelta(days=1)
    ]

    timeIntervalsBetweenPrices: list[str] = [
        "30m", "1h", "4h"
    ]

    priceCounts: list[int] = [
        48 + 1, 168 + 1, 186 + 1
    ]

    def __init__(self):
        pass

class ParametersOnHugeDistance(ParametersToModellingInterface):
    modellingName: str = "HANDLE PRICES ON HUGE DISTANCE"

    parsingDatetimes: list[tuple[datetime, datetime]] = [
        (CURRENT_TIME-timedelta(days=9), CURRENT_TIME-timedelta(days=1)),
        (CURRENT_TIME-timedelta(days=40), CURRENT_TIME-timedelta(days=1)),
        (CURRENT_TIME-timedelta(days=280), CURRENT_TIME-timedelta(days=1))
    ]

    endDatetimesToModellingPredict: list[datetime] = [
        CURRENT_TIME-timedelta(days=2),
        CURRENT_TIME-timedelta(days=8),
        CURRENT_TIME-timedelta(days=32)
    ]

    timeIntervalsBetweenPrices: list[str] = [
        "30m", "2h", "12h"
    ]

    priceCounts: list[int] = [
        384 + 1, 468 + 1, 558 + 1
    ]

    def __init__(self):
        pass