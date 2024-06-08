from polynom import *
from spline import *


def read_table(filename):
    f = open(filename, 'r')
    tbl = []
    for line in f:
        tbl.append(list(map(float, line.rstrip().split())))

    f.close()
    return tbl


if __name__ == '__main__':
    n = 3
    table = read_table('data.txt')
    x = float(input("Введите x: "))

    working_table = choose_points(table, x, n)
    newton_sub_table = newton_divided_differences(working_table)
    newton_value = calc_value(newton_sub_table, x)
    print(f'Полином Ньютона: y({x}) = {round(newton_value, 7)}')

    # естественные краевые условия
    start_1, end_1 = 0, 0

    # на одной границе - производная полинома Ньютона 3й степени
    start_2, end_2 = find_derivative(newton_sub_table, working_table[0][0]), 0

    # на двух границах - производная полинома Ньютона 3й степени
    start_3, end_3 = find_derivative(newton_sub_table, working_table[0][0]), find_derivative(newton_sub_table,
                                                                                             working_table[-1][0])
    spline_value_1 = spline(table, x, start_1, end_1)
    print(f'Сплайн с естественными краевыми условиями:\n\ty({x}) = {round(spline_value_1, 7)}')
    spline_value_2 = spline(table, x, start_2, end_2)
    print(f'Сплайн со 2й производной на левой границе равной 2й производной полинома Ньютона 3й степени:\n\ty({x}) = '
          f'{round(spline_value_2, 7)}')
    spline_value_3 = spline(table, x, start_3, end_3)
    print(f'Сплайн со 2ми производными на обеих границах равными 2м производным полинома Ньютона 3й степени:\n\ty({x}) '
          f'= {round(spline_value_3, 7)}')
