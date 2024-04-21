import numpy as np
import matplotlib.pyplot as plt
import Device.GaussianDevice as gd
import Filter.filter1D as f1d
import PhysicalPhenomena.sinus_distance as sd

import importlib
importlib.reload(gd)
importlib.reload(f1d)

total_time = 400    #[s]
time_res = 0.1
base_dist = 0    # [m]
amplitude = 2    # [m]
noise_std = 0
zero_vel = 0.1       # [m/s]

phenomenon = sd.SinusDistance(base_dist, amplitude, zero_vel)
device = gd.GaussianDevice(noise_std, phenomenon)

filter = f1d.SimpleFilter1D(
    delay = 0,
    min_length = 0.02,
    in_points = False,
    order = 1,
    length = 15)

time = np.linspace(0, total_time, int(total_time*(1/time_res))) 
time_res = time[1] - time[0]

pos = np.zeros(time.size)
pos_est = np.zeros(time.size)
for i in range(time.size):
    device.UpdateState(time[i])
    pos[i] = device.getMeasurement()
    if i==0:
        filter.AddMeasurement(0, pos[i])
    else:
        filter.AddMeasurement(time_res, pos[i])
    est = filter.GetFitResult(0)
    if est is not None:
        pos_est[i] = est[0]

plt.plot(time, pos)
plt.plot(time, pos_est)
plt.show()