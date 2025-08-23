from cryptocurrencymanager import CryptocurrencyManager
from datetime import datetime
from datetimeparser import (getDatetimeFrom,
                            getTimeIntervalFrom)
from general import TimeIntervalValidDiapasons

class DataInputerOfGraphicScreen:
    __cryptocurrency: str
    __startDatetime: datetime
    __endDatetime: datetime
    __futureDatetime: datetime
    __timeInterval: str
    __timeIntervalInMs: int
    __cryptocurrencyManager: CryptocurrencyManager

    def __init__(self, cryptocurrencyManager: CryptocurrencyManager):
        self.__cryptocurrencyManager = cryptocurrencyManager

    def input(self):
        """
        Requests a data fields: start date, end date, future date and time interval with validation
        """
        self.__inputCryptocurrencySymbol()

        print("Enter dates.")
        self.__inputStartDatetime()
        self.__inputEndDatetime()
        self.__inputFutureDatetime()

        print("Input time interval, for example 5m, 1h, 1d and etc:", end=" ")
        self.__inputTimeInterval()

    def __inputCryptocurrencySymbol(self):
        run: bool = True

        print("Input the cryptocurrency symbol:", end=" ")
        while(run):
            self.__cryptocurrency: str = input().upper()
            if(self.__cryptocurrencyManager.existsOnMarket(self.__cryptocurrency)):
                run = False
            else:
                print("Error. You have probably entered the wrong currency!")
                print("Try again:", end=" ")

    def __inputStartDatetime(self):
        run = True
        while(run):
            print("Start date:", end=" ")
            try:
                self.__startDatetime: datetime = getDatetimeFrom(input())
                run = False
            except ValueError:
                print("Error. Not valid format!")
                print("Try again.")

    def __inputEndDatetime(self):
        run = True
        while(run):
            print("End date:", end=" ")
            try:
                self.__endDatetime: datetime = getDatetimeFrom(input())

                if(self.__startDatetime < self.__endDatetime):
                    run = False
                else:
                    print("Error. The start date must be earlier than the end date!")
                    print("Try again.")

            except ValueError:
                print("Error. Not valid format!")
                print("Try again.")

    def __inputFutureDatetime(self):
        run = True
        while(run):
            print("Future date:", end=" ")
            try:
                self.__futureDatetime: datetime = getDatetimeFrom(input())

                if(self.__endDatetime < self.__futureDatetime):
                    run = False
                else:
                    print("Error. The end date must be earlier than the future date!")
                    print("Try again.")
                    
            except ValueError:
                print("Error. Not valid format!")
                print("Try again.")

    def __inputTimeInterval(self):
        run = True
        while(run):
            self.__timeInterval = input()

            timeIntervalParsingResult: tuple[str, int] = getTimeIntervalFrom(self.__timeInterval,
                                                                             minutes=TimeIntervalValidDiapasons.minutes,
                                                                             hours=TimeIntervalValidDiapasons.hours,
                                                                             days=TimeIntervalValidDiapasons.days)

            if(timeIntervalParsingResult[0] == 'm'):
                print(f"Error. Format minutes is nm, where n biggers or equals {TimeIntervalValidDiapasons.minutes[0]} and less or equals {TimeIntervalValidDiapasons.minutes[1]}.")
                print("Try again:", end=" ")
            
            elif(timeIntervalParsingResult[0] == 'h'):
                print(f"Error. Format hours is nh, where n biggers or equals {TimeIntervalValidDiapasons.hours[0]} and less or equals {TimeIntervalValidDiapasons.hours[1]}.")
                print("Try again:", end=" ")
            
            elif(timeIntervalParsingResult[0] == 'd'):
                print(f"Error. Format days is nd, where n biggers or equals {TimeIntervalValidDiapasons.days[0]} and less or equals {TimeIntervalValidDiapasons.days[1]}.")
                print("Try again:", end=" ")
            
            elif(timeIntervalParsingResult[1] == -1):
                print("Error. Not valid format!")
                print("Try again:", end=" ")

            else:
                self.__timeIntervalInMs = timeIntervalParsingResult[1]
                run = False

    @property
    def cryptocurrencySymbol(self):
        return self.__cryptocurrency
    
    @property
    def startDatetime(self):
        return self.__startDatetime
    
    @property
    def endDatetime(self):
        return self.__endDatetime
    
    @property
    def futureDatetime(self):
        return self.__futureDatetime
    
    @property
    def timeInterval(self):
        return self.__timeInterval
    
    @property
    def timeIntervalInMs(self):
        return self.__timeIntervalInMs