from datetime import datetime
from dataclasses import dataclass

@dataclass
class CryptocurrencyInformation:
    symbol: str
    startDatetimes: list[datetime]
    endDatetimes: list[datetime]
    futureDatetimes: list[datetime]
    timeIntervals: list[tuple[str, int]]