from .graphicscreen import (FirstScreenExecutor,
                            SecondScreenExecutor,
                            FifthScreenExecutor)
from .manypricesscreen import (ThirdScreenExecutor,
                               FourthScreenExecutor,
                               SixthScreenExecutor)
from .exitscreen import ExitScreenExecutor
from .executor import ScreenExecutor
from .general import (FILE_NAME_WITH_CRYPTOCURRENCIES,
                      LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC,
                      LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES)

VALID_SCREEN_NUMBERS: list[int] = [i for i in range(1, 8)]

EXECUTORS: dict[int, ScreenExecutor] = {
    1: FirstScreenExecutor(),
    2: SecondScreenExecutor(),
    3: ThirdScreenExecutor(),
    4: FourthScreenExecutor(),
    5: FifthScreenExecutor(),
    6: SixthScreenExecutor(),
    7: ExitScreenExecutor()
}

def printVersion():
    print("DESKTOP VERSION")

def printMenuScreen():
    firstCommand: str = "Show graphic of one cryptocurrency"
    secondCommand: str = f"Get prediction prices from '{FILE_NAME_WITH_CRYPTOCURRENCIES}'"

    print("MENU:")
    print(f"1. {firstCommand}")
    print(f"2. {firstCommand} with logging in '{LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC}'")
    print(f"3. {secondCommand}")
    print(f"4. {secondCommand} with logging in '{LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES}'")
    print(f"5. {firstCommand} documentation")
    print(f"6. {secondCommand} documentation")
    print("7. Exit")

def inputScreenNumberFromMenu() -> int:
    print("Input screen number:", end=" ")
    inputedVariant: str = input()
    while(not inputedVariant.isdigit() or int(inputedVariant) not in VALID_SCREEN_NUMBERS):
        print(f"Error. Need input the integer number biggers or equals {VALID_SCREEN_NUMBERS[0]} and less or equals {VALID_SCREEN_NUMBERS[-1]}!")
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
    """
    Output last words
    """
    print("Program work ended.")