from abc import (ABC,
                 abstractmethod)

class ScreenExecutor(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()
    
    @abstractmethod
    def execute(self) -> bool:
        raise NotImplementedError()