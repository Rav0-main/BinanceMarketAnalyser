from dataclasses import dataclass

@dataclass
class TimeIntervalValidDiapasons:
    minutes: tuple[int, int] = (1, 59)
    hours: tuple[int, int] = (1, 23)
    days: tuple[int, int] = (1, 30)

@dataclass
class DeltaDatetimeValidDiapasons:
    minutes: tuple[int, int] = (1, 59)
    hours: tuple[int, int] = (1, 23)
    days: tuple[int, int] = (1, 365 * 2)

FILE_NAME_WITH_CRYPTOCURRENCIES: str = "to-predict.json"
STR_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"