import numpy as np
from Sensor.ISensor import ISensor
from Observable.IObservable import IObservable

class GaussianSensor(ISensor):
    def __init__(self, noise_std:float, phenomenon: IObservable) -> float:
        super().__init__(phenomenon)
        self.noise_std = noise_std
    

    # def update(self, time: float) -> float:
    #     return self.phenomenon.getMeasurableState()


    def realize(self) -> float:
        noise = np.random.normal(0, self.noise_std)
        return self.state + noise