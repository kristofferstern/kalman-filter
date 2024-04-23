import numpy as np
from Device.device import Device
from PhysicalPhenomena.IPhysicalPhenomenon import IPhysicalPhenomenon

class GaussianDevice(Device):
    def __init__(self, noise_std:float, phenomenon: IPhysicalPhenomenon) -> float:
        super().__init__(phenomenon)
        self.noise_std = noise_std
    

    def update(self, time: float) -> float:
        return self.phenomenon.getMeasurableState()


    def realize(self) -> float:
        noise = np.random.normal(0, self.noise_std)
        return self.state + noise