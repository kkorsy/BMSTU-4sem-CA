def multidimensional_interpolation(matrix, x_list, y_list, z_list, x, y, z, interp_x, interp_y, interp_z):
    z_values = []
    for k in range(len(z_list)):
        y_values = []
        for i in range(len(y_list)):
            x_values = []
            for j in range(len(x_list)):
                x_values.append([x_list[j], matrix[k][i][j]])
            print('x: ', end=' ')
            print(x_values)

            y_values.append([y_list[i], interp_x(x_values, x)])
        print('y: ', end=' ')
        print(y_values)

        z_values.append([z_list[k], interp_y(y_values, y)])
    print('z: ', end=' ')
    print(z_values)

    return interp_z(z_values, z)
