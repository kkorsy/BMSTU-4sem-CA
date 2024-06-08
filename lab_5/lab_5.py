import numpy
from sympy import symbols, diff
from math import pi, sqrt, exp
import matplotlib.pyplot as plt

eps = 1e-7


# x^2 + y^2 + z^2 - 1 = 0
# 2x^2 + y^2 - 4z = 0
# 3x^2 - 4y + z^2 = 0
def solve_system():
    # вектор начального приближения
    xk = [1, 1, 1]

    x, y, z = symbols('x y z')
    f1 = x ** 2 + y ** 2 + z ** 2 - 1
    f2 = 2 * x ** 2 + y ** 2 - 4 * z
    f3 = 3 * x ** 2 - 4 * y + z ** 2

    num_vars = 3
    list_vars, list_func = [x, y, z], [f1, f2, f3]
    matrix = numpy.zeros((num_vars, num_vars))
    res = numpy.zeros(num_vars)

    delta = 1
    while delta > eps:
        # матрица линейной системы относительно delta_xk
        for i in range(num_vars):
            for j in range(num_vars):
                expr = diff(list_func[i], list_vars[j])
                matrix[i][j] = expr.evalf(subs={list_vars[j]: xk[j]})
            res[i] = -(list_func[i].evalf(subs={list_vars[0]: xk[0],
                                                list_vars[1]: xk[1],
                                                list_vars[2]: xk[2]}))

        delta_xk = numpy.linalg.solve(matrix, res)

        next_xk = numpy.zeros(num_vars)
        new_delta = -1

        # следующее приближение
        for i in range(num_vars):
            next_xk[i] = xk[i] + delta_xk[i]
            new_delta = max(new_delta, abs(next_xk[i] - xk[i]))     # текущая точность

        # замена предыдущих значений
        for i in range(num_vars):
            xk[i] = next_xk[i]
        delta = new_delta

    print('Решение системы:')
    print(f'\tx = {xk[0]}\n\ty = {xk[1]}\n\tz = {xk[2]}')


def integrate(bottom, top):
    def f(t):
        return exp(-(t ** 2) / 2)

    n = 50
    x = numpy.linspace(bottom, top, n)
    h = (top - bottom) / n

    res = f(x[0]) + f(x[n - 1])
    for i in range(1, n):
        res += f(x[i]) * 2
    res *= (h / 2)

    return res


def func(x):
    return (2 / (sqrt(2 * pi))) * integrate(0, x)


def find_arg():
    y = float(input('\nВведите значение функции: '))

    a, b = -10, 10
    while b - a > eps:
        c = (a + b) / 2
        if (func(b) - y) * (func(c) - y) < 0:
            a = c
        else:
            b = c

    print(f'\nf({(a + b) / 2}) = {y}')
    print('Найденная абсцисса:')
    print(f'\tx = {(a + b) / 2}')


def print_graph(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()


# y'' - y^3 = x^2
# x = 0, y = 1
# x = 1, y = 3
def solve_diff():
    def start_func(t):
        return 2 * t + 1

    def f(xn, yn):
        return yn ** 3 + xn ** 2

    def derivative_f(yn):
        return 3 * yn ** 2

    # начальное приближение
    a, b, n = 0, 1, 50
    h = (b - a) / n
    x = numpy.linspace(a, b, n)
    yk = [1]
    for i in range(1, n - 1):
        yk.append(start_func(x[i]))
    yk.append(3)

    matrix = numpy.zeros((n, n))
    res = numpy.zeros(n)

    delta = 1
    while delta > eps:
        # заполняем матрицу
        k = 0
        for i in range(n):
            if k != 0:
                matrix[i][k - 1] = 1
            matrix[i][k] = -(2 + h ** 2 * derivative_f(yk[k]))
            if k != n - 1:
                matrix[i][k + 1] = 1
            k += 1

        k = 1
        res[0] = 0
        for i in range(1, n - 1):
            res[i] = -(yk[k - 1] - 2 * yk[k] + yk[k + 1] - h ** 2 * f(x[k], yk[k]))
            k += 1
        res[n - 1] = 0

        delta_yk = numpy.linalg.solve(matrix, res)

        next_yk = numpy.zeros(n)
        new_delta = -1

        # следующее приближение
        for i in range(n):
            next_yk[i] = yk[i] + delta_yk[i]
            new_delta = max(new_delta, abs(next_yk[i] - yk[i]))  # текущая точность

        # замена предыдущих значений
        for i in range(n):
            yk[i] = next_yk[i]
        delta = new_delta

    print_graph(x, yk)


if __name__ == '__main__':
    solve_system()
    find_arg()
    solve_diff()
