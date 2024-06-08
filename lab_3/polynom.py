import numpy as np


def choose_points(tbl, degree, point):
    tbl.sort()
    working_tbl = []
    closest_value, ind = tbl[0][0], 0

    # найти ближайшее табличное
    for i in tbl:
        if abs(point - i[0]) < abs(point - closest_value):
            closest_value = i[0]
            ind = tbl.index(i)

    # заполнить таблицу
    working_tbl.append(tbl[ind])
    c, sign_swaped = 1, False
    while len(working_tbl) < degree + 1:
        cur = ind + c
        if len(tbl) > cur >= 0:
            working_tbl.append(tbl[cur])
        if not sign_swaped:
            c = -c
            sign_swaped = True
        else:
            c = -c
            c += 1
            sign_swaped = False

    working_tbl.sort()
    return working_tbl


def newton_divided_differences(tbl):
    sub_table = np.zeros((len(tbl), len(tbl) + 1))
    # заполнить начальными значениями
    for i in range(len(tbl)):
        for j in range(len(tbl[i])):
            sub_table[i][j] = tbl[i][j]

    # разделенные разности
    for column in range(2, len(sub_table[0])):
        for line in range(column - 1, len(sub_table)):
            sub_table[line][column] = (sub_table[line - 1][column - 1] - sub_table[line][column - 1]) / \
                                      (sub_table[line - column + 1][0] - sub_table[line][0])

    return sub_table


def calc_value(sub_table, point):
    value = sub_table[0][1]
    mul = 1
    for i in range(2, len(sub_table[0])):
        mul *= (point - sub_table[i - 2][0])
        value += mul * sub_table[i - 1][i]

    return value


def newton_interpolate(table, n, x):
    working_table = choose_points(table, n, x)
    sub_table = newton_divided_differences(working_table)

    return calc_value(sub_table, x)
