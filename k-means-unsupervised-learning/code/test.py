import numpy as np

arr = np.array([1, 2, 3])
nan_arr = np.array([np.nan, np.nan, np.nan])
test = np.power(np.sum(np.power(arr - nan_arr, 2), axis = 0), 0.5)
print(nan_arr.astype(int))