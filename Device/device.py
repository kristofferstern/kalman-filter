import abc
from PhysicalPhenomena.IPhysicalPhenomenon import IPhysicalPhenomenon

class Device(metaclass=abc.ABCMeta):
    def __init__(self, phenomenon: IPhysicalPhenomenon) -> None:
        self.time = 0
        self.state = 0
        self.phenomenon = phenomenon


    @abc.abstractmethod
    def realize(self):
        pass


    @abc.abstractmethod
    def update(self, time: float):
        pass


    def UpdateState(self, time: float):
        self.time = time
        self.phenomenon.UpdateState(time)
        self.state = self.update(time)


    def getMeasurement(self) -> float:
        value = self.realize()
        return value