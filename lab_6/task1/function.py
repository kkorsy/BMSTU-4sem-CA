from scipy.interpolate import RectBivariateSpline
from scipy.integrate import dblquad
import numpy as np
from readfile import x_values, y_values, z_values
DELTA = 1e-7


# Интерполяция функции z=f(x, y) по таблице
def f(x, y):
    # Используем выравнивающие переменные (n, x, y), где n = ln(z)
    n_values = np.log(z_values)
    
    # Интерполяция функции z=f(x, y) по таблице с использованием выравнивающих переменных (n, x, y)
    spline = RectBivariateSpline(x_values, y_values, n_values)
    interpolated_n = spline.ev(x, y)
    
    # Обратное преобразование для получения значения функции z=f(x, y)
    interpolated_z = np.exp(interpolated_n)
    
    return interpolated_z
