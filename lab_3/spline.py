def spline(table, x, start=0, end=0):
    x_list = list(i[0] for i in table)
    y_list = list(i[1] for i in table)

    h_list = find_h(x_list)

    a = find_a(y_list)
    c = find_c(x_list, y_list, h_list, start, end)
    b = find_b(y_list, h_list, c)
    d = find_d(c, h_list)

    ind = get_index(x_list, x)
    b.append(0)
    c.append(0)
    d.append(0)

    return a[ind] + b[ind] * (x - x_list[ind]) + c[ind] * (x - x_list[ind]) ** 2 + \
           d[ind] * (x - x_list[ind]) ** 3


def get_index(x_list, point):
    # ind = 0
    # while ind < len(x_list) - 1 and x_list[ind] < point:
    #     ind += 1

    ind = None
    for i in range(len(x_list)):
        if x_list[i] >= point:
            ind = i
            break

    if ind is None:
        ind = -1

    return ind


def find_a(y_list):
    a_list = list()
    for i in range(len(y_list)):
        a_list.append(y_list[i])

    return a_list


def find_b(y_list, h_list, c_list):
    b = list()
    for i in range(len(c_list) - 1):
        b.append((y_list[i] - y_list[i - 1]) / h_list[i + 1] - (1 / 3) * h_list[i + 1] * (c_list[i + 1] + 2 * c_list[i]))

    return b


def find_c(x_list, y_list, h_list, start, end):
    c = [0 for _ in range(len(x_list) + 2)]
    c[1] = start / 2
    c[-2] = end / 2

    d2_list = [0, 0] + list(h_list[i] for i in range(2, len(h_list)))
    b2_list = [0, 0] + list(-2 * (h_list[i - 1] + h_list[i]) for i in range(2, len(h_list)))
    a2_list = [0, 0] + list(h_list[i - 1] for i in range(2, len(h_list)))
    f_list = [0, 0] + find_f(y_list, h_list)

    m1, k1, p1 = 0, 1, start / 2

    ksi = find_ksi(d2_list, b2_list, a2_list, m1, k1)
    eta = find_eta(a2_list, f_list, b2_list, ksi, p1, k1)

    for i in range(len(c) - 2, 0, -1):
        c[i - 1] = ksi[i] * c[i] + eta[i]

    return c[1:-1]


def find_d(c_list, h_list):
    d = list()
    for i in range(len(c_list) - 1):
        d.append((c_list[i + 1] - c_list[i]) / (3 * h_list[i + 1]))

    return d


def find_h(x_list):
    h = [0]
    for i in range(1, len(x_list)):
        h.append(x_list[i] - x_list[i - 1])

    return h


def find_ksi(d2_list, b2_list, a2_list, m1, k1):
    ksi = [0, 0, -m1 / k1]
    for i in range(2, len(b2_list)):
        ksi.append(d2_list[i] / (b2_list[i] - a2_list[i] * ksi[i]))

    return ksi


def find_eta(a2_list, f_list, b2_list, ksi_list, p1, k1):
    eta = [0, 0, p1 / k1]
    for i in range(2, len(f_list)):
        eta.append((a2_list[i] * eta[i] + f_list[i]) / (b2_list[i] - a2_list[i] * ksi_list[i]))

    return eta


def find_f(y_list, h_list):
    f = list()
    for i in range(2, len(h_list)):
        f.append(-3 * ((y_list[i] - y_list[i - 1]) / h_list[i] - (y_list[i - 1] - y_list[i - 2]) / h_list[i - 1]))

    return f
