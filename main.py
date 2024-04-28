import numpy as np
import matplotlib.pyplot as plt
import Sensor.gaussian_sensor as gs
import Filter.filter1D as f1d
import Observable.sinus_distance as sin_dist

import importlib
importlib.reload(gs)
importlib.reload(f1d)

total_time = 400    #[s]
time_res = 0.1
base_dist = 1000    # [m]
amplitude = 1000    # [m]
noise_std = 16.0
zero_vel = 30       # [m/s]

observable = sin_dist.SinusDistance(base_dist, amplitude, zero_vel)
device = gs.GaussianSensor(noise_std, observable)


order = 1
filter = f1d.SimpleFilter1D(
    delay = 0,
    min_length = 0.02,
    in_points = False,
    order = order,
    length = 7)

time = np.linspace(0, total_time, int(total_time*(1/time_res))) 
time_res = time[1] - time[0]

state = np.zeros((time.size, order + 1))
state_est = np.zeros((time.size, order + 1))
for i in range(time.size):
    device.UpdateState(time[i])
    # pos[i] = device.getMeasurement()
    pos = device.getMeasurement()
    state[i, :] = observable.getState()
    if i==0:
        filter.AddMeasurement(0, pos)
    else:
        filter.AddMeasurement(time_res, pos)
    est = filter.GetFitResult(0)
    if est is not None:
        state_est[i,:] = est.flatten()

fig, axs = plt.subplots(order + 1)
fig.suptitle('Estimated states vs true states')
for i in range(order + 1):
    axs[i].plot(time, state[:, i])
    axs[i].plot(time, state_est[:, i])


plt.show()

# plt.plot(time, pos)
# plt.plot(time, pos_est)
# plt.show()