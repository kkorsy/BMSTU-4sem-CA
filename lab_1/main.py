import numpy as np


def read_table(filename):
    f = open(filename, 'r')
    tbl = []
    for line in f:
        tbl.append(list(map(float, line.rstrip().split())))

    f.close()
    return tbl


def choose_points(tbl, point, degree):
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


def sub_table_output(tbl):
    print('-' * (17 * len(tbl[0]) + 1))
    print('|{:^16}|{:^16}| Разделенные разности'.format('x', 'y'))
    print('-' * (17 * len(tbl[0]) + 1))
    for line in tbl:
        for elem in line:
            print('|{:^16.6f}'.format(elem), end='')
        print('|')
    print('-' * (17 * len(tbl[0]) + 1))


def newton_divided_differences(tbl):
    sub_table = np.zeros((len(tbl), len(tbl) + 1))
    # заполнить начальными значениями
    for i in range(len(tbl)):
        for j in range(len(tbl[i]) - 1):
            sub_table[i][j] = tbl[i][j]

    # разделенные разности
    for column in range(2, len(sub_table[0])):
        for line in range(column - 1, len(sub_table)):
            sub_table[line][column] = (sub_table[line - 1][column - 1] - sub_table[line][column - 1]) / \
                                      (sub_table[line - column + 1][0] - sub_table[line][0])

    return sub_table


def hermit_divided_differences(tbl):
    count_ys = 2
    sub_table = np.zeros((len(tbl) * count_ys, len(tbl) * count_ys + 1))
    # заполнить начальными значениями
    for line in range(len(tbl)):
        for count in range(count_ys):
            for column in range(len(tbl[line]) - 1):
                sub_table[line * count_ys + count][column] = tbl[line][column]

    # разделенные разности
    for column in range(2, len(sub_table[0])):
        for line in range(column - 1, len(sub_table)):
            if abs(sub_table[line - column + 1][0] - sub_table[line][0]) <= float(1e-7):
                sub_table[line][column] = tbl[line // count_ys][2]
            else:
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


def write_data(sub_tbl_1, sub_tbl_2):
    x_range = [i[0] for i in sub_tbl_2]
    f = open('diff_data.txt', 'w')
    for i in x_range:
        f.write(str(i) + ' ' + str(calc_value(sub_tbl_1, i) - calc_value(sub_tbl_2, i)) + ' 0\n')
    f.close()


notMonotone = 'notMonotone'
increasing = 'increasing'
decreasing = 'decreasing'


def get_type_of_monotone(tbl):
    is_increasing = True
    is_decreasing = True
    for row in range(len(tbl) - 1):
        if not (tbl[row][0] < tbl[row + 1][0] and tbl[row][1] < tbl[row + 1][1]):
            is_increasing = False
    for row in range(len(tbl) - 1):
        if not (tbl[row][0] > tbl[row + 1][0] and tbl[row][1] > tbl[row + 1][1]):
            is_decreasing = False
    if is_increasing:
        return increasing
    if is_decreasing:
        return decreasing
    return notMonotone


def get_root(tbl, monotone, case):
    new_table = np.zeros((len(tbl), len(tbl[0])))
    if monotone != notMonotone:
        for i in range(len(tbl)):
            new_table[i][0], new_table[i][1], new_table[i][2] = tbl[i][1], tbl[i][0], 0
        new_table = new_table.sort()
        subs = newton_divided_differences(new_table)
        return calc_value(subs, 0)
    else:
        if case == 'newton':
            subs = newton_divided_differences(tbl)
        else:
            subs = hermit_divided_differences(tbl)
        r = tbl[-1][0]
        l = tbl[0][0]
        while abs(r - l) > 1e-8:
            m = (r + l) / 2
            y = calc_value(subs, m)
            if y < 0:
                r = m
            else:
                l = m
        return (r + l) / 2


if __name__ == '__main__':
    table = read_table('data.txt')
    x = float(input('Введите x: '))
    n = int(input('Введите n: '))
    if n >= len(table):
        print("Недостаточно данных для построения")
        exit(1)

    working_table = choose_points(table, x, n)
    newton_sub_table = newton_divided_differences(working_table)
    hermit_sub_table = hermit_divided_differences(working_table)

    print('Разделенные разности для полинома Ньютона:')
    sub_table_output(newton_sub_table)
    print('Разделенные разности для полинома Эрмита:')
    sub_table_output(hermit_sub_table)

    newton_value = calc_value(newton_sub_table, x)
    print(f'Полином Ньютона: y({x}) = {round(newton_value, 7)}')
    hermit_value = calc_value(hermit_sub_table, x)
    print(f'Полином Эрмита:  y({x}) = {round(hermit_value, 7)}')

    # корень с помощью обратной интерполяции
    nr_root = get_root(working_table, get_type_of_monotone(working_table), 'newton')
    print(f'Корень с помощью полинома Ньютона: {round(nr_root, 7)}')
    hr_root = get_root(working_table, get_type_of_monotone(working_table), 'hermit')
    print(f'Корень с помощью полинома Эрмита:  {round(hr_root, 7)}')

    # решить систему
    n = 9
    table_1 = read_table('data_1.txt')
    table_2 = read_table('data_2.txt')

    sub_table_1 = newton_divided_differences(table_1)
    sub_table_2 = newton_divided_differences(table_2)

    # зависимость от разности
    write_data(sub_table_1, sub_table_2)
    diff_func = read_table('diff_data.txt')
    m = get_type_of_monotone(diff_func)
    res = get_root(diff_func, m, 'newton')

    print(f'Решение системы: x = {round(res, 7)}, y = {round(calc_value(sub_table_1, res), 7)}')
