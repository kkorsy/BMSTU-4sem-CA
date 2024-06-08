from interpolate import newton_polynomial


# Односторонняя разностная производная
def get_one_side(f, x, h):
    # Погрешность O(h)
    return (f(x + h) - f(x)) / h


# Центральная разностная производная
def get_central(f, x, h):
    # Погрешность O(h^2)
    return (f(x + h) - f(x - h)) / (2 * h)


# 2-я формула Рунге для численного дифференцирования с использованием односторонней разностной производной
def get_runge(f, x, h, m):
    # Погрешность O(h^p+1), где p - порядок точности используемой формулы
    # Для односторонней разностной производной p = 1 => O(h^2)
    phi_h = get_central(f, x, h)
    phi_mh = get_central(f, x, m * h)
    return phi_h + (phi_h - phi_mh) / (m - 1)


# Введены выравнивающие переменные
def get_fix_vars(f, x, h):
    # так как функция вида (a0 * x) / (a1 + a2 * x)
    # nu = 1 / y
    # ksi = 1 / x
    y = f(x)
    xh = x + h
    yh = f(xh)
    # diff = ((nu(y(i+1)) - nu(y(i))) * y^2) / ((ksi(x(i+1) / ksi(x)) * x^2)
    diff = (1 / yh - 1 / y) / (1 / xh - 1 / x) * y ** 2 / x ** 2
    return diff


# Вторая разностная производная
def get_second_diff(f, x, h):
    m = 2
    # Биномиальные коэффициенты
    coeffs = [1, -2, 1]
    res = 0
    for i in range(m + 1):
        res += coeffs[i] * f(x + (m / 2 - i) * h)
    return res / h**m


if __name__ == '__main__':
    x_list = [1, 2, 3, 4, 5, 6]
    y_list = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
    # Функция вида (a0 * x) / (a1 + a2 * x)
    h = 1e-6

    func = newton_polynomial(x_list, y_list)

    one_size, central, runge, fix_vars, second_diff = [], [], [], [], []

    for vx in x_list:
        one_size.append(get_one_side(func, vx, h))
        central.append(get_central(func, vx, h))
        runge.append(get_runge(func, vx, h, 2))
        fix_vars.append(get_fix_vars(func, vx, h))
        second_diff.append(get_second_diff(func, vx, h))

    print('Односторонняя:\n', one_size)
    print('Центральная:\n', central)
    print('2-я формула Рунге\n', runge)
    print('Выравнивающие переменные\n', fix_vars)
    print('Вторая производная\n', second_diff)
