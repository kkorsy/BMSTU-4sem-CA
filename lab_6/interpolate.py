# Эта функция вычисляет коэффициенты полинома Ньютона
# для заданных точек данных (x, y).
# x - массив значений x
# y - массив значений y
import numpy as np


def __poly_newton_coefficient(x, y):
    m = len(x)
    x = np.copy(x)
    a = np.copy(y)

    # Вычисляем разделенную разность порядка k для всех (k, m) значений
    for k in range(1, m):
        for i in range(k, m):
            a[i] = (a[i] - a[k - 1]) / (x[i] - x[k - 1])

    return a


# Эта функция создает полином функции на основе коэффициентов.
# a - массив коэффициентов полинома
# x_data - массив значений x
# n - степень полинома
def _create_polynomial_function(a, x_data, n=None):
    if n is None:
        n = len(x_data) - 1
    n = min(len(x_data) - 1, n)

    def res(x):
        p = a[n]
        for k in range(1, n + 1):
            idx = n - k
            p = a[idx] + (x - x_data[idx]) * p
        return p

    return res


# Эта функция возвращает полином Ньютона для заданных точек данных (x_data, y_data).
# x_data - массив значений x
# y_data - массив значений y
# n - степень полинома
def newton_polynomial(x_data, y_data, n=None):
    a = __poly_newton_coefficient(x_data, y_data)

    return _create_polynomial_function(a, x_data, n)