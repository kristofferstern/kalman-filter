import numpy as np
from collections import deque

from Filter.IFilter import IFilter

class FadingMemoryFilter1D:

    @staticmethod
    def __characteristic_time(filter_length: float) -> None:
        return filter_length / 2.3

    def __init__(self, order: float, length: float) -> None:
        self.__order = order
        self.__length = length
        self.__tau = self.__characteristic_time(length)
        self.__state_estimate = np.zeros((1,1))
        self.__state_covariance_estimate = np.zeros((1,1))
        self.__initialized = False
        self.__initialization_time_series = []


    def AddMeasurement(self, step_length, measurement) -> bool:
        if not self.__initialized:
            for i in range(len(self.__initialization_time_series)):
                self.__initialization_time_series[i][0] -= step_length

            self.__initialization_time_series.append([0.0, measurement])

            if (len(self.__initialization_time_series) == self.__order + 1):
                self.__Initialize()
        else:
            self.__UpdateFilter(step_length, measurement)

        return self.__initialized


    def GetStateEstimate(self, step_length: float) -> np.array:
        if self.__initialized:
            A = np.zeros((self.__order + 1, self.__order + 1))
            for row in range(self.__order + 1):
                A[row, row] = 1.0
                for column in range(row + 1, self.__order + 1):
                    A[row, column] = A[row, column - 1] * step_length / (column-row)

            predictedState = A.dot(self.__state_estimate)
            return predictedState
        else:
            return None


    def ChangeLength(self, new_length: float) -> None:
        self.__tau = self.__characteristic_time(new_length)


    def __Initialize(self) -> None:
        N = len(self.__initialization_time_series)
        assert N == self.__order + 1, f"initialization time series lenght ({N}) does not match filter order ({self.__order})."

        H_i = np.ones((N,N))
        z_i = np.ones((N, 1))

        for i in range(N):
            time, measurement = self.__initialization_time_series[i]
            for j in range(1, N):
                H_i[i,j] = H_i[i,j-1] * time/j
            z_i[i,0] = measurement
        
        H_inv = np.linalg.inv(H_i)

        self.__state_estimate = np.matmul(H_inv, z_i)
        self.__state_covariance_estimate = np.matmul(H_inv, np.transpose(H_inv)) 
        self.__initialized = True
        self.__initialization_time_series = []


    def __UpdateFilter(self, step: float, measurement: float) -> None:
        assert self.__initialized, "Trying to update uninitialized fading memory filter"
        A = np.zeros((self.__order + 1, self.__order + 1))
        for row in range(self.__order + 1):
            A[row, row] = 1.0
            for column in range(row + 1, self.__order + 1):
                A[row, column] = A[row, column - 1] * step / (column-row)
        
        #### Prediction step
        x_1 = A.dot(self.__state_estimate)
        temp = np.matmul(self.__state_covariance_estimate, np.transpose(A))
        P_1 = np.matmul(A, temp)
        #### Re-equilabration for stability
        P_1 = (P_1 + np.transpose(P_1)) * 0.5

        #### Fade the past memory by scaling the uncertainty (with a sanity maximum introudced)
        P_1 = P_1 * np.exp(min(step / self.__tau, 10.0))

        C = np.zeros((1, self.__order + 1))
        C[0,0] = 1.0
        R = 1.0
        K = (np.matmul(P_1, np.transpose(C))) * (1.0/(P_1[0,0] + R))

        #### Update state estimate
        self.__state_estimate = x_1 + K * (measurement - x_1[0,0])

        #### Update uncertainty estimate 
        self.__state_covariance_estimate = P_1 - np.matmul(K, np.transpose(K)) * (P_1[0,0] + R)
        

class SimpleFilter1D(IFilter):
    def __init__(self, delay: float, min_length: float, in_points: bool, order: int, length: float) -> None:
        self.__filter = FadingMemoryFilter1D(order, length)
        self.__filter_length = length
        self.__input_times = deque([])
        self.__requirements_in_points = False
        self.__remaining_delay_points = 0
        self.__remaining_delay_length = 0.0
        self.__min_points = 0
        self.__min_length = 0.0
        self.__cummulative_points = 0
        self.__cummulative_length = 0.0
        self.__first_data_received = False
        self.ChangeSettings(delay, min_length, in_points, length)


    def ChangeSettings(self, delay: float, min_length: float, in_points: bool, fit_length: float) -> None:
        self.__filter.ChangeLength(fit_length)
        self.__filter_length = fit_length
        self.__requirements_in_points = in_points
        self.__cummulative_length = 0.0
        self.__cummulative_points = 0
        if in_points:
            self.__remaining_delay_length = 0.0
            self.__min_length = 0.0
            self.__remaining_delay_points = int(delay)
            self.__min_points = int(min_length)
        else:
            self.__remaining_delay_length = delay
            self.__min_length = min_length
            self.__remaining_delay_points = 0
            self.__min_points = 0


    def AddMeasurement(self, step: float, measurement: np.array) -> bool:
        for i in range(len(self.__input_times)):
            self.__input_times[i] -= step
        
        while len(self.__input_times) > 0 and self.__input_times[0] < -self.__filter_length:
            self.__input_times.popleft()

        self.__input_times.append(0.0)

        if (self.__requirements_in_points and self.__remaining_delay_points > 0):
            self.__remaining_delay_points -= 1
            return True
        elif not self.__requirements_in_points and self.__remaining_delay_length > 0.0 and self.__first_data_received:
            self.__remaining_delay_length -= step
            return True
        
        if self.__remaining_delay_points == 0 and self.__remaining_delay_length <= 0.0:
            if self.__first_data_received:
                self.__cummulative_length += step
            self.__cummulative_points += 1
            self.__filter.AddMeasurement(step, measurement)
        
        self.__first_data_received = True
        return True



    def GetFitResult(self, step: float) -> np.array:
        state = self.__filter.GetStateEstimate(step)
        valid = state is not None
        
        if self.__requirements_in_points:
            valid = valid and self.__cummulative_points >= self.__min_points and len(self.__input_times) >= self.__min_points
        else:
            if len(self.__input_times) == 0:
                return False
            front_time = max(self.__input_times[0], step - self.__filter_length)
            time_diff = self.__input_times[-1] - front_time
            valid = valid and time_diff >= self.__min_length and self.__remaining_delay_length <= 0 and self.__cummulative_length >= self.__min_length
        
        if (valid):
            return state
        else:
            return None

    