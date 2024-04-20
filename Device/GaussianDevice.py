import numpy as np
from Device.device import Device

class GaussianDevice(Device):
    def __init__(self, base_distance, amplitude, noise_std) -> float:
        super().__init__()
        self.base_distance = base_distance
        self.amplitude = amplitude
        self.noise_std = noise_std
    
    def update(self, time: float) -> float:
        return self.amplitude * np.sin(2 * np.pi * 1/100 * time) + self.base_distance

    def realize(self) -> float:
        noise = np.random.normal(0, self.noise_std)
        return self.state + noise