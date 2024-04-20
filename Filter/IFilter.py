import abc

class IFilter(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def ChangeSettings(self, dealy: float, min_length: float, in_points: bool, fit_length: float):
        pass

    @abc.abstractmethod
    def AddMeasurement(self, step: float, measurement: float):
        pass

    @abc.abstractmethod
    def GetFitResult(self, step: float):
        pass