import abc

class Device(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.time = 0
        self.state = 0


    @abc.abstractmethod
    def realize(self):
        pass


    @abc.abstractmethod
    def update(self, time: float):
        pass


    def UpdateState(self, time: float):
        self.time = time
        self.state = self.update(time)


    def getMeasurement(self) -> float:
        value = self.realize()
        return value