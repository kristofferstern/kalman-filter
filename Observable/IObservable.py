import abc
import numpy as np

class IObservable(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.time = 0
        self.state = np.array([])


    @abc.abstractmethod
    def realize(self):
        pass


    @abc.abstractmethod
    def update(self, time: float):
        pass


    def UpdateState(self, time: float) -> None:
        self.time = time
        self.state = self.update(time)


    def getMeasurableState(self) -> float:
        value = self.realize()
        return value
    

    def getState(self) -> np.array:
        return self.state