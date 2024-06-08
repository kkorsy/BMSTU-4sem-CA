from prettytable import PrettyTable
from gauss import *
from function import *

N_MAX = 14
M_MAX = 14
x_left = 0
x_right = 1
y_bottom = 0
y_top = 1

table = PrettyTable(['Кол-во узлов'] + list(range(1, M_MAX)))
for n in range(1, N_MAX):
    string = [n]
    for m in range(1, M_MAX):
        string.append(f'{gauss_integ(n, m, x_left, x_right, y_bottom, y_top, f):f}')
    table.add_row(string)
print(table)
