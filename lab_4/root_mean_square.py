from numpy.linalg import solve
from numpy import zeros, linspace, meshgrid, array
from matplotlib import pyplot as plt


def draw_graph(table, f):
    x_min, x_max = min(list(p[0] for p in table)), max(list(p[0] for p in table))
    x_values = linspace(x_min, x_max, 40)

    plt.figure("График(и) функции, полученный аппроксимации наименьших квадратов")
    plt.ylabel("Y")
    plt.xlabel("X")

    y_values = f(x_values)
    plt.plot(x_values, y_values, 'k', label="y = f(x)")

    for p in table:
        plt.plot(p[0], p[1], 'r.')

    plt.legend()
    plt.show()


def one_dimensional(table):
    n = int(input('Введите степень полинома: ')) + 1

    matrix = zeros((n, n))
    res = zeros(n)
    for i in range(n):
        for j in range(n):
            s = 0
            for p in table:
                s += p[2] * p[0] ** (i + j)
            matrix[i][j] = s

        s = 0
        for p in table:
            s += p[2] * p[1] * p[0] ** i
        res[i] = s

    koefs = solve(matrix, res)

    def f(x):
        y = 0
        for k in range(len(koefs)):
            y += koefs[k] * x ** k
        return y

    draw_graph(table, f)


def make_3d_matrix(table, n):
    a, b = list(), list()
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a_row = []
            for k in range(n + 1):
                for t in range(n + 1 - k):
                    s = 0
                    for p in table:
                        s += (p[0] ** (k + i) * p[1] ** (t + j)) * p[-1]
                    a_row.append(s)
            a.append(a_row)
            s = 0
            for p in table:
                s += (p[0] ** i * p[1] ** j) * p[2] * p[-1]
            b.append(s)
    matrix = list()
    for i in range(len(a)):
        matrix.append(a[i])
    return matrix, b


def draw_3d_graph(table, f):
    min_x, max_x = min(list(p[0] for p in table)), max(list(p[0] for p in table))
    min_y, max_y = min(list(p[1] for p in table)), max(list(p[1] for p in table))

    x_values = linspace(min_x, max_x, 40)
    y_values = linspace(min_y, max_y, 40)

    def make_grid():
        # Создаем двумерную матрицу-сетку
        x_grid, y_grid = meshgrid(x_values, y_values)
        # В узлах рассчитываем значение функции
        z_grid = array([[f(x_grid[i][j], y_grid[i][j]) for j in range(len(x_values))] for i in range(len(y_values))])
        return x_grid, y_grid, z_grid

    fig = plt.figure("График функции, полученный аппроксимации наименьших квадратов")
    xpoints, ypoints, zpoints = list(p[0] for p in table), list(p[1] for p in table), list(p[2] for p in table)
    axes = fig.add_subplot(projection='3d')
    axes.scatter(xpoints, ypoints, zpoints, c='red')
    axes.set_xlabel('OX')
    axes.set_ylabel('OY')
    axes.set_zlabel('OZ')
    x_values, y_values, z_values = make_grid()
    axes.plot_surface(x_values, y_values, z_values)
    plt.show()


def two_dimensional(table):
    n = 1
    matrix, res = make_3d_matrix(table, n)
    koefs = solve(matrix, res)

    def f(x, y):
        result = 0
        c_index = 0
        for i in range(n + 1):
            for j in range(n + 1 - i):
                result += koefs[c_index] * (x ** i * y ** j)
                c_index += 1
        return result

    draw_3d_graph(table, f)
