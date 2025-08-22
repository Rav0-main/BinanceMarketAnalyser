from .graphicscreen import (GraphicViewerScreenWithoutLogging,
                            GraphicViewerScreenWithLogging,
                            DocumentationScreenOfGraphicViewer,
                            LoggingOutputerOfGraphicViewerScreen)
from .manypricesscreen import (ManyPricesScreenViewerWithoutLogging,
                               ManyPricesScreenViewerWithLogging,
                               DocumentationScreenOfManyPricesViewer,
                               LoggingOutputerOfManyPricesViewerScreen)
from .exitscreen import ExitScreenExecutor
from .executor import ScreenExecutor
from .general import (FILE_NAME_WITH_CRYPTOCURRENCIES,
                      LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC,
                      LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES)

VALID_SCREEN_NUMBERS: list[int] = [i for i in range(1, 10)]

EXECUTORS: dict[int, ScreenExecutor] = {
    1: GraphicViewerScreenWithoutLogging(),
    2: GraphicViewerScreenWithLogging(),
    3: LoggingOutputerOfGraphicViewerScreen(),

    4: ManyPricesScreenViewerWithoutLogging(),
    5: ManyPricesScreenViewerWithLogging(),
    6: LoggingOutputerOfManyPricesViewerScreen(),

    7: DocumentationScreenOfGraphicViewer(),
    8: DocumentationScreenOfManyPricesViewer(),
    
    9: ExitScreenExecutor()
}

def printVersion():
    print("DESKTOP VERSION")

def printMenuScreen():
    firstCommand: str = "View graphic of one cryptocurrency"
    secondCommand: str = f"View prediction prices from '{FILE_NAME_WITH_CRYPTOCURRENCIES}'"
    thirdCommand: str = f"Output logging content of"

    print("MENU:")
    print(f"1. {firstCommand}")
    print(f"2. {firstCommand} with logging in '{LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC}'")
    print(f"3. {thirdCommand} '{LOGGING_FILE_OF_SCREEN_WITH_GRAPHIC}'")
    print(f"4. {secondCommand}")
    print(f"5. {secondCommand} with logging in '{LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES}'")
    print(f"6. {thirdCommand} '{LOGGING_FILE_OF_SCREEN_WITH_MANY_PRICES}'")
    print(f"7. {firstCommand} documentation")
    print(f"8. {secondCommand} documentation")
    print("9. Exit")

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