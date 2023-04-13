from scipy.optimize import minimize
import numpy as np

def __linear_resdiuals(parameters, dataset):
    x = np.array(dataset[0])
    y = np.array(dataset[1])
    y_approx = parameters[0] * x + parameters[1] 
    residual = np.abs(y - y_approx)
    return np.sum(residual**2)

def optimize_parameters(m, sq_angle):
    optimized_linear = minimize(__linear_resdiuals, [0.00005, 1e-5], [m, sq_angle]).x
    return optimized_linear