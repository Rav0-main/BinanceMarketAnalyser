from .executor import ScreenExecutor

class ExitScreenExecutor(ScreenExecutor):
    def __init__(self):
        pass

    def execute(self) -> bool:
        print("Thanks for use!")
        return True