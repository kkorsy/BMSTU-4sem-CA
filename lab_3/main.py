from multi_interp import multidimensional_interpolation
from polynom import newton_interpolate
from spline import spline


def get_n():
    return int(input("Введите степень nx: ")), int(input("Введите степень ny: ")), int(input("Введите степень nz: "))


def input_data():
    try:
        x, y, z = float(input("Введите аргумент x: ")), float(input("Введите аргумент y: ")), \
                  float(input("Введите аргумент z: "))
        interp = int(input("Способы интерполяции:\n\t1) Полиномами Ньютона\n\t2) Сплайнами\n\t3) Смешанная\n\n"
                           "Выберите номер способа интерполяции: "))
        return x, y, z, interp
    except ValueError:
        print("Введены некорректные данные")
        return 0, 0, 0, 0, 0, 0


def read_table(filename):
    f = open(filename, 'r')
    x_list, y_list, z_list = [], [], []
    matrix = [[[0] * 5 for _ in range(5)] for _ in range(5)]
    i_m, j_m = -1, 0
    for line in f:
        if 'z=' in line:
            s = line.strip().split('z=')
            z_list.append(float(s[1]))
            i_m += 1
            j_m = 0
        elif 'y\\x' in line:
            if i_m == 0:
                s = line.strip().split('y\\x')[1].strip().split('\t')
                x_cur = list(map(float, s))
                for i in x_cur:
                    x_list.append(i)
        elif len(line.strip()) != 0:
            cur_list = list(map(float, line.rstrip().split()))
            if i_m == 0:
                y_list.append(cur_list[0])
            del cur_list[0]
            for k in range(len(cur_list)):
                matrix[i_m][j_m][k] = cur_list[k]
            j_m += 1

    f.close()
    return x_list, y_list, z_list, matrix


if __name__ == '__main__':
    x_list, y_list, z_list, matrix = read_table('data.txt')
    x, y, z, interp_way = input_data()

    nx = ny = nz = None
    if interp_way == 1:
        nx, ny, nz = get_n()
        interp_x = lambda table, p: newton_interpolate(table, nx, p)
        interp_y = lambda table, p: newton_interpolate(table, ny, p)
        interp_z = lambda table, p: newton_interpolate(table, nz, p)
    elif interp_way == 2:
        interp_x = interp_y = interp_z = spline
    else:
        nx, ny, nz = get_n()
        interp_x = lambda table, p: newton_interpolate(table, nx, p)
        interp_y = spline
        interp_z = lambda table, p: newton_interpolate(table, nz, p)

    u = multidimensional_interpolation(matrix, x_list, y_list, z_list, x, y, z, interp_x, interp_y, interp_z)
    print('\nРезультат интерполяции:')
    print(f"f({x}, {y}, {z}) = {u}")
