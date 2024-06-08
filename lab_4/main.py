from random import randint
from root_mean_square import *
from difur_solve import dif_solve
from numpy import linspace


def read_table():
    filename = input('Введите имя файла: ')
    f = open(filename)
    tbl = []
    for line in f:
        tbl.append(list(map(float, line.rstrip().split())))
    f.close()
    return tbl


def generate_fx():
    def f(x):
        return x ** 3
    xn, xk = float(input('Введите начало отрезка: ')), float(input('Введите конец отрезка: '))
    n = int(input('Введите количество точек: '))
    x_list = linspace(xn, xk, n)
    tbl = list()

    for i in x_list:
        tbl.append([i, f(i), randint(1, 5)])

    return tbl


def generate_fxy():
    def f(x, y):
        return x ** 2 / 4 - y ** 2 / 9

    xn, xk = float(input('Введите начало отрезка X: ')), float(input('Введите конец отрезка X: '))
    nx = int(input('Введите количество точек X: '))
    yn, yk = float(input('Введите начало отрезка Y: ')), float(input('Введите конец отрезка Y: '))
    ny = int(input('Введите количество точек Y: '))
    x_list = linspace(xn, xk, nx)
    y_list = linspace(yn, yk, ny)

    tbl = list()

    for i in x_list:
        for j in y_list:
            tbl.append([i, j, f(i, j), randint(1, 5)])

    return tbl


def print_table(table):
    flag_z = False
    if len(table[0]) == 4:
        flag_z = True

    if flag_z:
        print('_' * 43)
        print('|  №  |    x    |    y    |    z    | Вес |')
        print('_' * 43)
        for i in range(len(table)):
            print('|{:^5}|{:^9}|{:^9}|{:^9}|{:^5}|'.format(i + 1, round(table[i][0], 3), round(table[i][1], 3),
                                                           round(table[i][2], 3), table[i][3]))
        print('_' * 43)
    else:
        print('_' * 33)
        print('|  №  |    x    |    y    | Вес |')
        print('_' * 33)
        for i in range(len(table)):
            print('|{:^5}|{:^9}|{:^9}|{:^5}|'.format(i + 1, round(table[i][0], 3), round(table[i][1], 3), table[i][2]))
        print('_' * 33)


def change_weight(table):
    i = int(input('Введите номер точки, вес которой хотите изменить: '))
    w = int(input(f'Введите вес {i}-й точки: '))
    table[i - 1][-1] = w

    return table


def set_one_weight(table):
    for i in table:
        i[-1] = 1

    return table


def print_menu():
    menu = '''Меню:
    1. Считать таблицу из файла
    2. Сгенерировать таблицу f(x)
    3. Сгенерировать таблицу f(x, y)
    4. Вывести таблицу
    5. Изменить вес точки
    6. Установить все веса равные 1
    7. Вывести график 
    8. Решить ОДУ второго порядка
    0. Выйти из программы
    '''
    print(menu)
    return int(input("Выберите пункт меню: "))


if __name__ == '__main__':
    data_table = None

    cmd = print_menu()
    while cmd:
        if cmd == 1:
            data_table = read_table()
        elif cmd == 2:
            data_table = generate_fx()
        elif cmd == 3:
            data_table = generate_fxy()
        elif cmd == 4:
            print_table(data_table)
        elif cmd == 5:
            data_table = change_weight(data_table)
        elif cmd == 6:
            data_table = set_one_weight(data_table)
        elif cmd == 7:
            if len(data_table[0]) == 3:
                one_dimensional(data_table)
            elif len(data_table[0]) == 4:
                two_dimensional(data_table)
        elif cmd == 8:
            dif_solve()
        else:
            print('Такой команды нет')
        cmd = print_menu()
