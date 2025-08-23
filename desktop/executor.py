from os import path as osPath
from sys import path as sysPath

rootDirectory = osPath.dirname(osPath.abspath(__file__))
sysPath.append(rootDirectory)

from abc import (ABC,
                 abstractmethod)
from os import (system,
                rename,
                remove)
from re import findall
from datetime import (datetime,
                      timedelta)
from general import STR_DATE_FORMAT
from cryptocurrencymanager import (CryptocurrencyManager,
                                   CryptocurrencyInputParseProtocol)
from time import sleep
from typing import TextIO

class ScreenExecutor(ABC):
    """
    Parent class of each screen executor.
    """
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()
    
    @abstractmethod
    def execute(self) -> bool:
        raise NotImplementedError()
    
class ScreenOfLoggingOutputer(ScreenExecutor):
    """
    Parent class of each screen with logging output
    """
    _loggingFileName: str
    _cryptocurrencyManager: CryptocurrencyManager

    __isOpenPrice: bool = False
    __currentCryptocurrency: str = ""
    __parsedCount: int = 0
    __parsingCycle: int = 4
    __sleepTime: float = 2.0
    __newLoggingFile: TextIO
    __priceAndDatetimeRegExp = r'(\d+\.\d+)\$ \((\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\)'
    __datetimeRegExp = r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}'
    
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()
    
    def execute(self) -> bool:
        system("cls")

        if(not osPath.exists(self._loggingFileName)):
            print(f"Error. File with name {self._loggingFileName} not found!")
            return False

        newLoggingFileName = self._loggingFileName[:self._loggingFileName.index(".")] + "-temporary.txt"
        self.__newLoggingFile = open(newLoggingFileName, "w")

        with open(self._loggingFileName, "r") as file:
            i: int = 0
            fileLines: list[str] = file.readlines()
            fileLinesLen: int = len(fileLines)

            while(i < fileLinesLen):
                i += self.__handleLine(fileLines, i)
                    
        self.__newLoggingFile.close()

        remove(self._loggingFileName)
        rename(newLoggingFileName, self._loggingFileName)

        self.__parsedCount = 0
        print("\n")
        print("Press <Enter> to continue")
        input()
        
        return False
    
    def __handleLine(self, lines: list[str], index: int) -> int:
        line = lines[index]
        notNeedPrint: bool = False
        if(line.startswith("PREDICTION: ")):
            startIndex: int = len("PREDICTION: ")
            self.__currentCryptocurrency = line[startIndex:-2]
            self.__printCryptocurrencySymbol()
            notNeedPrint = True

        elif(line.startswith("1. Open Price:")):
            self.__isOpenPrice = True
            self.__printPriceType()
            notNeedPrint = True

        elif(line.startswith("2. Close Price:")):
            self.__isOpenPrice = False
            self.__printPriceType()
            notNeedPrint = True

        elif(line.startswith("Datetime moment:")):
            self.__printDatetimeMoment(line)
            notNeedPrint = True

        elif(line.startswith("Datetime interval:")):
            self.__printDatetimeInterval(line)
            notNeedPrint = True

        if(notNeedPrint):
            self.__newLoggingFile.write(line)
            notNeedPrint = False
            return 1

        matchesByPattern = findall(self.__priceAndDatetimeRegExp, line)

        if(len(matchesByPattern) == 0):
            print(line, end="")
            self.__newLoggingFile.write(line)
            return 1

        leftPriceValue: float = float(matchesByPattern[0][0])
        leftDatetimeStr: str = matchesByPattern[0][1]
                                            

        rightPriceValue: float = float(matchesByPattern[-1][0])
        rightDatetimeStr: str = matchesByPattern[-1][1]
                    
        if(line.startswith("Predict.")):
            if(self.__isDatetimeToCheckPrediction(datetime.strptime(rightDatetimeStr, STR_DATE_FORMAT))):
                self.__printRealPriceWithParsingRealPrice((leftDatetimeStr, leftPriceValue),
                                                              (rightDatetimeStr, rightPriceValue))
                            
                return 2
            else:
                self.__printPrediction((leftDatetimeStr, leftPriceValue),
                                            (rightDatetimeStr, rightPriceValue))
                            
                return 2

        else:
            nextLine: str = lines[index+1]
            matchesByPattern = findall(self.__priceAndDatetimeRegExp, nextLine)
                        
            predictedPriceValue: float = float(matchesByPattern[0][0])
            predictedDatetimeStr: str = matchesByPattern[0][1]
                        
            self.__printRealPriceWithoutParsingRealPrice((leftDatetimeStr, leftPriceValue),
                                                             (predictedDatetimeStr, predictedPriceValue),
                                                             rightPriceValue)
            return 3
    
    def __printCryptocurrencySymbol(self):
        print("PREDICTION: ", end="")
        print("\033[1m", self.__currentCryptocurrency, "\033[0m", sep="")

    def __printPriceType(self):
        line: str = ""
        if(self.__isOpenPrice):
            line = "\033[3m\033[92m1. Open Price\033[0m:"
        else:
            line = "\033[3m\033[91m2. Close Price\033[0m:"

        print(line)

    def __printDatetimeMoment(self, line: str):
        print("Datetime moment: ", end="")
        datetimeMomentStr: str = findall(self.__datetimeRegExp, line)[0]
        print("\033[1m\033[96m", datetimeMomentStr, "\033[0m.", sep="")

    def __printDatetimeInterval(self, line: str):
        print("Datetime interval: ", end="")
        datetimeInterval = findall(self.__datetimeRegExp, line)

        print("\033[96m", datetimeInterval[0], " - ", datetimeInterval[1], "\033[0m.", sep="")
    
    def __isDatetimeToCheckPrediction(self, forecastDatetime: datetime):
        return datetime.now() >= forecastDatetime
    
    def __printRealPriceWithParsingRealPrice(self, pastPrice: tuple[str, float], predictedPrice: tuple[str, float]):
        self.__parsedCount += 1

        if(self.__parsedCount % self.__parsingCycle == 0):
            sleep(self.__sleepTime)

        priceInformation = self._cryptocurrencyManager.parse(
            CryptocurrencyInputParseProtocol(
                self.__currentCryptocurrency, (datetime.strptime(predictedPrice[0], STR_DATE_FORMAT),
                                               datetime.strptime(predictedPrice[0], STR_DATE_FORMAT) + timedelta(minutes=1)),
                ("1m", 1 * 60 * 1000)
            )
        )[0]

        realPriceValue: float = priceInformation.open if self.__isOpenPrice else priceInformation.close
            
        self.__printRealPriceWithoutParsingRealPrice(pastPrice, predictedPrice, realPriceValue)

    def __printPrediction(self, lastPrice: tuple[str, float], predictionPrice: tuple[str, float]):
        print(f"\033[43m\033[30mPredict.\033[0m Price from \033[95m{lastPrice[1]:.3f}$\033[0m ({lastPrice[0]}) move to \033[33m{predictionPrice[1]:.3f}$\033[0m ({predictionPrice[0]}).")
        print(f"Relative difference: \033[1m\033[97m{(predictionPrice[1] - lastPrice[1])/lastPrice[1]*100:.3f}%\033[0m.")

        self.__newLoggingFile.write(f"Predict. Price from {lastPrice[1]:.3f}$ ({lastPrice[0]}) move to {predictionPrice[1]:.3f}$ ({predictionPrice[0]}).\n")
        self.__newLoggingFile.write(f"Relative difference: {(predictionPrice[1] - lastPrice[1])/lastPrice[1]*100:.3f}%.\n")

    def __printRealPriceWithoutParsingRealPrice(self, pastPrice: tuple[str, float], predictedPrice: tuple[str, float], realPriceValue: float):
        print(f"\033[42m\033[30mReal.\033[0m Price from \033[95m{pastPrice[1]:.3f}$\033[0m ({pastPrice[0]}) move to \033[32m{realPriceValue:.3f}$\033[0m ({predictedPrice[0]}).")
        print(f"But predicted price - \033[34m{predictedPrice[1]:.3f}$\033[0m ({predictedPrice[0]}).")
        print(f"Relative difference between real and predicted: \033[1m\033[97m{(realPriceValue - predictedPrice[1])/realPriceValue*100:.3f}%\033[0m.")

        self.__newLoggingFile.write(f"Real. Price from {pastPrice[1]:.3f}$ ({pastPrice[0]}) move to {realPriceValue:.3f}$ ({predictedPrice[0]}).\n")
        self.__newLoggingFile.write(f"But predicted price - {predictedPrice[1]:.3f}$ ({predictedPrice[0]}).\n")
        self.__newLoggingFile.write(f"Relative difference between real and predicted: {(realPriceValue - predictedPrice[1])/realPriceValue*100:.3f}%.\n")