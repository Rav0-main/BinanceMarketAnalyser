from datetime import (datetime,
                      timedelta)
from .general import DeltaDatetimeValidDiapasons

def getDatetimeFrom(string: str) -> datetime:
    if(string.startswith("now")):
        startDatetime: datetime = datetime.now()
        i: int = 3
        while(i < len(string) and string[i] == ' '):
            i += 1

        if(i == len(string)):
            return startDatetime
        
        sign: int = 1
        if(string[i] == '-'):
            sign = -1

        i += 1
        while(i < len(string) and string[i] == ' '):
            i += 1

        if(i == len(string)):
            return startDatetime
        
        timeInterval: str = ""
        while(i < len(string) and (string[i] != 'm' or string[i] != 'h' or string != 'd')):
            timeInterval = timeInterval + string[i]
            i += 1

        timeIntervalInMs: int = getTimeIntervalFrom(timeInterval)[1]
        if(timeIntervalInMs == -1):
            return startDatetime
        else:
            return startDatetime + sign * timedelta(milliseconds=timeIntervalInMs)
        
    return datetime.fromisoformat(string)
        
def getTimeIntervalFrom(string: str, minutes: tuple[int, int] = DeltaDatetimeValidDiapasons.minutes,
                        hours: tuple[int, int] = DeltaDatetimeValidDiapasons.hours,
                        days: tuple[int, int] = DeltaDatetimeValidDiapasons.days) -> tuple[str, int]:
    
    timeIntervalInMs: int = -1
    minutesValidDiaposon: tuple[int, int] = minutes
    hoursValidDiaposon: tuple[int, int] = hours
    daysValidDiaposon: tuple[int, int] = days
    
    if("m" in string):
        value: str = string[:string.index("m")]
        if(not value.isdigit() or int(value) < minutesValidDiaposon[0] or int(value) > minutesValidDiaposon[1]):
            return ("m", -1)
        else:
            timeIntervalInMs = int(value) * 60 * 1000
            
    elif("h" in string):
        value: str = string[:string.index("h")]
        if(not value.isdigit() or int(value) < hoursValidDiaposon[0] or int(value) > hoursValidDiaposon[1]):
            return ("h", -1)
        else:
            timeIntervalInMs = int(value) * 60 * 60 * 1000

    elif("d" in string):
        value: str = string[:string.index("d")]
        if(not value.isdigit() or int(value) < daysValidDiaposon[0] or int(value) > daysValidDiaposon[1]):
            return ("d", -1)
        else:
            timeIntervalInMs = int(value) * 24 * 60 * 60 * 1000

    return (string, timeIntervalInMs)