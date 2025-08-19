from abc import (ABC,
                 abstractmethod)

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