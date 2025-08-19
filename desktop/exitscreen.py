from .executor import ScreenExecutor

class ExitScreenExecutor(ScreenExecutor):
    """
    An output screen executor that simply displays the last words and returns True.
    """
    def __init__(self):
        pass

    def execute(self) -> bool:
        print("Thanks for use!")
        return True