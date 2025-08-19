from .firstscreen import *
from .secondscreen import *
from .exitscreen import*
from .executor import ScreenExecutor
from .general import FILE_NAME_WITH_CRYPTOCURRENCIES

VALID_SCREEN_NUMBERS: list[int] = [i for i in range(1, 6)]

EXECUTORS: dict[int, ScreenExecutor] = {
    1: FirstScreenExecutor(),
    2: SecondScreenExecutor(),
    5: ExitScreenExecutor()
}

def printVersion():
    print("DESKTOP VERSION")

def printMenuScreen():
    firstCommand: str = "Show graphic of one cryptocurrency"
    secondCommand: str = f"Get prediction prices from '{FILE_NAME_WITH_CRYPTOCURRENCIES}'"
    print("MENU:")
    print(f"1. {firstCommand}")
    print(f"2. {secondCommand}")
    print(f"3. {firstCommand} --help")
    print(f"4. {secondCommand} --help")
    print("5. Exit")

def inputScreenNumberFromMenu() -> int:
    print("Input screen number:", end=" ")
    inputedVariant: str = input()
    while(not inputedVariant.isdigit() or int(inputedVariant) not in VALID_SCREEN_NUMBERS):
        print("Error. Need input the integer number biggers or equals 1 and less or equals 3!")
        print("Try again:", end=" ")
        inputedVariant = input()

    return int(inputedVariant)

def compelete(variant: int) -> bool:
    """
    Returns True if need exit from program else False
    """
    if(variant not in EXECUTORS):
        print(f"Error. Not valid variant of executing: {variant}.")
        return False
    
    return EXECUTORS[variant].execute()

def printExit():
    print("Program work ended.")