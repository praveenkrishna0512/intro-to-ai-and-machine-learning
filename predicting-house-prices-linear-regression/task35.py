# Inital imports and setup

import os
import numpy as np

###################
# Helper function #
###################
def load_data(filepath):
    '''
    Load in the given csv filepath as a numpy array

    Parameters
    ----------
    filepath (string) : path to csv file

    Returns
    -------
        X, y (np.ndarray, np.ndarray) : (m, num_features), (m,) numpy matrices
    '''
    *X, y = np.genfromtxt(
        filepath,
        delimiter=',',
        skip_header=True,
        unpack=True,
    ) # default dtype: float
    X = np.array(X, dtype=np.float64).T # cast features to int type
    return X, y.reshape((-1, 1))

data_filepath = 'housing_data.csv'
X, y = load_data(data_filepath)

def mean_squared_error(y_target, y_pred):
    '''
    Calculate mean squared error between y_pred and y_target.

    Parameters
    ----------
    y_target (np.ndarray) : (m, 1) numpy matrix consists of target values
    y_pred (np.ndarray)   : (m, 1) numpy matrix consists of predictions
    
    Returns
    -------
        The mean squared error value.
    '''
  
    # TODO: add your solution here and remove `raise NotImplementedError`
    y_diff = np.subtract(y_pred, y_target)
    y_squared = np.power(y_diff, 2)
    y_sum = np.sum(y_squared)
    return y_sum / (2 * y_target.size)


def add_bias_column(X):
    '''
    Create a bias column and combined it with X.

    Parameters
    ----------
    X : (m, n) numpy matrix representing feature matrix
    
    Returns
    -------
        A (m, n + 1) numpy matrix with the first column consists of all 1
    '''
  
    column_length = X.shape[0]
    bias_column = np.ones((column_length, 1))
    result = np.concatenate((bias_column, X), axis=1)
    return result

def change_in_weight(y_target, y_pred, X, lr):
    '''
    Calculate the required change in weights

    Parameters
    ----------
    y_target (np.ndarray) : (m, 1) numpy matrix consists of target values
    y_pred (np.ndarray)   : (m, 1) numpy matrix consists of predictions
    X (np.ndarray) : (m, n) numpy matrix representing feature matrix
    lr (float) : Learning rate
    
    Returns
    -------
        The required change in weights, as an array.
    '''
  
    y_diff = np.subtract(y_pred, y_target)
    y_mult_x = X * y_diff
    sum_of_y_mult_x = np.sum(y_mult_x, axis=0).reshape((X.shape[1] , 1))
    return lr * (sum_of_y_mult_x / y_target.size)

def find_number_of_iterations(X, y, lr, delta_loss):
    '''
    Do gradient descent until convergence and return number of iterations
    required.

    Parameters
    ----------
    X (np.ndarray) : (m, n) numpy matrix representing feature matrix
    y (np.ndarray) : (m, 1) numpy matrix representing target values
    lr (float) : Learning rate
    delta_loss (float) : Termination criterion
    
    Returns
    -------
        bias (float):
            The bias constant
        weights (np.ndarray):
            A (n, 1) numpy matrix that specifies the weight constants.
        num_of_iterations (int):
            Number of iterations to reach convergence
    '''
    # Do not change
    bias = 0
    weights = np.full((X.shape[1], 1), 0).astype(float)
    num_of_iterations = 0
    previous_loss = 1e14
    current_loss = -1e14

    weights_arr = np.concatenate(([[bias]], weights))
    X = add_bias_column(X)
    y_pred = X @ weights_arr
    while abs(previous_loss - current_loss) >= delta_loss:
        num_of_iterations += 1
        change_in_weight_arr = change_in_weight(y, y_pred, X, lr)
        weights_arr = weights_arr - change_in_weight_arr
        y_pred = X @ weights_arr
        previous_loss = current_loss
        current_loss = mean_squared_error(y, y_pred)
    
    return weights_arr[0][0], np.delete(weights_arr, 0, 0), num_of_iterations


def feature_scaling(X):
    '''
    Mean normalized each feature column.

    Parameters
    ----------
    X (np.ndarray) : (m, n) numpy matrix representing feature matrix

    Returns
    -------
        A (m, n) numpy matrix where each column has been mean-normalized.
    '''
    # TODO: add your solution here and remove `raise NotImplementedError`
    standard_dev = np.std(X, axis=0)
    mean = np.mean(X, axis=0)
    result = (X - mean) / standard_dev
    return result

def create_polynomial_matrix(X, power = 2):
    '''
    Create a polynomial matrix.
    
    Parameters
    ----------
    X: (m, 1) numpy matrix

    Returns
    -------
        A (m, power) numpy matrix where the i-t h column denotes
            X raised to the power of i.
    '''
    power_arr = np.arange(1, power + 1)
    return np.power(X, power_arr)

def run(poly_X = None, mean_norm_poly_X = None, y = None, lr_arr = None):
    for lr in lr_arr:
        print(f"Running for learning rate: {lr}")
        if poly_X != None:
            _, _, poly_i = find_number_of_iterations(poly_X, y, lr, 1e7)
            print(f"Poly: {poly_i}")
        if mean_norm_poly_X != None:
            _, _, mean_norm_i = find_number_of_iterations(mean_norm_poly_X, y, lr, 1e7)
            print(f"Mean Norm: {mean_norm_i}")

poly_X = create_polynomial_matrix(X[:, 2].reshape((-1, 1)), 3)
mean_norm_poly_X = feature_scaling(poly_X)
# run(poly_X, mean_norm_poly_X, y, [1e-20, 1e-15])
# run(poly_X, mean_norm_poly_X, y, [1e-7, 1e-6])
# run(poly_X, mean_norm_poly_X, y, [1e-5, 1e-4])
# run(poly_X, mean_norm_poly_X, y, [1e-3, 1e-2])
# run(poly_X, mean_norm_poly_X, y, [1e-1, 1])
# run(mean_norm_poly_X, y, [4e-6, 5e-6, 8e-6,])
run(None, mean_norm_poly_X, y, [1e-3])
run(None, mean_norm_poly_X, y, [1e-2])
run(None, mean_norm_poly_X, y, [1e-1])
# run(poly_X, mean_norm_poly_X, y, [1])