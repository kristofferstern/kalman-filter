import numpy as np
from Observable.IObservable import IObservable

class SinusDistance(IObservable):
    def __init__(self, base_distance: float, amplitude: float, zero_vel: float) -> float:
        super().__init__()
        self.base_distance = base_distance
        self.amplitude = amplitude
        self.x = zero_vel / (2 * np.pi * amplitude)


    def update(self, time: float) -> float:
        state = np.array([
            self.amplitude * np.sin(2 * np.pi * self.x * time) + self.base_distance,
            self.amplitude * np.pi * self.x * np.cos(2 * np.pi * self.x * time)
        ])
        return state


    def realize(self) -> float:
        #### Return the observable state of the distanse observable
        #### Here it is only distance (not higher orders)
        return self.state[0]