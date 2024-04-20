import numpy as np
import matplotlib.pyplot as plt
import Device.GaussianDevice as gd
import Filter.filter1D as f1d
# from GaussianDevice import GaussianDevice
# from filter1D import SimpleFilter1D

import importlib
importlib.reload(gd)
importlib.reload(f1d)

total_time = 400
time_res = 0.1
base_dist = 0
amplitude = 2
noise_std = 0.1

device = gd.GaussianDevice(base_dist, amplitude, noise_std)
filter = f1d.SimpleFilter1D(
    delay = 0,
    min_length = 0.02,
    in_points = False,
    order = 2,
    length = 15)

time = np.linspace(0, total_time, int(total_time*(1/time_res))) 
pos = np.zeros(time.size)
bob = np.zeros(time.size)
for i in range(time.size):
    device.UpdateState(time[i])
    pos[i] = device.getMeasurement()
    if i==0:
        filter.AddMeasurement(0, pos[i])
    else:
        filter.AddMeasurement(time_res, pos[i])
    john = filter.GetFitResult(0)
    if john is not None:
        bob[i] = john[0]

plt.plot(time, pos)
plt.plot(time, bob)
plt.show()