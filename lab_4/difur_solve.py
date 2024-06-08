from numpy import linspace, zeros
from numpy.linalg import solve
from scipy.misc import derivative
from matplotlib import pyplot as plt
# y'' + xy' + y = 2x
# y(0) = 1; y(1) = 0


def find_derivative(f, point, n):
    y_n = derivative(f, point, dx=1e-7, n=n)
    return y_n


def y(x, m, d):
    s = zeros(m)
    for i in range(m):
        s[i] = find_derivative(lambda x: base_func(x, i + 1), x, d)
    return s, find_derivative(lambda x: base_func(x, 0), x, d)


def base_func(x, k):
    return x ** (2 * k) * (1 - x)


# def alpha(x):
#     return -4 * x ** 3 + 3 * x ** 2 - 6 * x + 2
#
#
# def beta(x):
#     return -6 * x ** 5 + 5 * x ** 4 - 20 * x ** 3 + 12 * x ** 2
#
#
# def teta(x):
#     return -x ** 7 - 6 * x ** 6 - 36 * x ** 5 + 30 * x ** 4
#
#
# def gamma(x):
#     return 4 * x - 1


def dif_solve():
    x_set = linspace(0, 1, 5)

    m = 2
    matrix = zeros((m, m))
    res = zeros((m, 1))

    for x in x_set:
        alpha, beta, gamma = 0, 0, 0
        for i in range(m):
            cur, r = y(x, m, i + 1)
            alpha += cur[0]
            beta += cur[1]
            gamma += r
        matrix[0][0] += alpha ** 2
        matrix[0][1] += alpha * beta
        res[0][0] += alpha * gamma
        matrix[1][0] += alpha * beta
        matrix[1][1] += beta ** 2
        res[1][0] += beta * gamma

        # matrix[0][0] += alpha(x) ** 2
        # matrix[0][1] += alpha(x) * beta(x)
        # res[0][0] += alpha(x) * gamma(x)
        # matrix[1][0] += alpha(x) * beta(x)
        # matrix[1][1] += beta(x) ** 2
        # res[1][0] += beta(x) * gamma(x)

    koefs = solve(matrix, res)

    def res_func1(x):
        return base_func(x, 0) + koefs[0] * base_func(x, 1) + koefs[1] * base_func(x, 2)

    m = 3
    matrix = zeros((m, m))
    res = zeros((m, 1))

    for x in x_set:
        alpha, beta, teta, gamma = 0, 0, 0, 0
        for i in range(2):
            cur, r = y(x, m, i + 1)
            alpha += cur[0]
            beta += cur[1]
            teta += cur[2]
            gamma += r

        matrix[0][0] += alpha ** 2
        matrix[0][1] += alpha * beta
        matrix[0][2] += alpha * teta
        res[0][0] += alpha * gamma

        matrix[1][0] += alpha * beta
        matrix[1][1] += beta ** 2
        matrix[1][2] += beta * teta
        res[1][0] += beta * gamma

        matrix[2][0] += alpha * teta
        matrix[2][1] += beta * teta
        matrix[2][2] += teta ** 2
        res[2][0] += gamma * teta

        # matrix[0][0] += alpha(x) ** 2
        # matrix[0][1] += alpha(x) * beta(x)
        # matrix[0][2] += alpha(x) * teta(x)
        # res[0][0] += alpha(x) * gamma(x)
        #
        # matrix[1][0] += alpha(x) * beta(x)
        # matrix[1][1] += beta(x) ** 2
        # matrix[1][2] += beta(x) * teta(x)
        # res[1][0] += beta(x) * gamma(x)
        #
        # matrix[2][0] += alpha(x) * teta(x)
        # matrix[2][1] += beta(x) * teta(x)
        # matrix[2][2] += teta(x) ** 2
        # res[2][0] += gamma(x) * teta(x)

    koefs = solve(matrix, res)

    def res_func2(x):
        return base_func(x, 0) + koefs[0] * base_func(x, 1) + koefs[1] * base_func(x, 2) + koefs[2] * base_func(x, 3)

    draw_graph(res_func1, res_func2, x_set)


def draw_graph(f1, f2, x_values):
    plt.figure("График(и) функции, полученный аппроксимации наименьших квадратов")
    plt.ylabel("Y")
    plt.xlabel("X")

    y_values = f1(x_values)
    plt.plot(x_values, y_values, 'k', label="y = f1(x)")

    y_values = f2(x_values)
    plt.plot(x_values, y_values, 'r', label="y = f2(x)")

    plt.legend()
    plt.show()
