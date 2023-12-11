from time import time


def monitor(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        try:
            result = func(*args, **kwargs)
        except:
            print(f'Function {func.__name__!r} executed in {(time() - t1):.16f}s')
            return
        print(f'Function {func.__name__!r} executed in {(time() - t1):.16f}s')
        return result

    return wrap_func


Game = object
value_of_cell = []
constraint_on_cell = []


@monitor
def simple_solve(game):
    # print(game.data_fills)
    global Game
    global value_of_cell
    Game = game
    for i in range(9):
        row = []
        constraint = []
        for j in range(9):
            if [i, j] not in game.data_fills:
                row.append((0, 0))
                constraint.append([(-1, -1), (-1, -1)])
            else:
                row.append(0)
                constraint.append([(-1, -1), (-1, -1)])
        constraint_on_cell.append(constraint)
        value_of_cell.append(row)
    # print("value of cell :", value_of_cell)
    for cell in game.data_totals:
        i, j = cell[2], cell[3]
        if isinstance(value_of_cell[i][j], tuple):
            _x, _y = value_of_cell[i][j]
            if cell[1] == 'v':
                value_of_cell[i][j] = (_x, _y + cell[0])
            else:
                value_of_cell[i][j] = (_x + cell[0], _y)
        else:
            _x, _y = 0, 0
            if cell[1] == 'v':
                value_of_cell[i][j] = (_x, _y + cell[0])
            else:
                value_of_cell[i][j] = (_x + cell[0], _y)

    for cell in game.data_fills:
        x, y = cell[0], cell[1]
        xi, yi = get_left_consist(x, y)
        xj, yj = get_up_consist(x, y)
        constraint_on_cell[x][y] = [(xi, yi), (xj, yj)]

    back_track(0)
    return Game.data_filled


def back_track(current_cell_index):
    global Game
    global value_of_cell
    # print(len(Game.data_filled))
    if current_cell_index == len(Game.data_fills):
        if Game.check_win():
            print(' ACCEPTED ')
            return True
        else:
            # print(' FAILED ')
            # print_mp()
            return False
    current_cell = Game.data_fills[current_cell_index]
    for i in range(9):
        # print(" ********************* ")
        Game.data_filled += [[current_cell[0], current_cell[1], i + 1]]
        value_of_cell[current_cell[0]][current_cell[1]] = i + 1
        if update_filled_sum_value(current_cell[0], current_cell[1]):
            # print(" ****** ++++++++++++++++++++++++++++++++++")
            if back_track(current_cell_index + 1):
                return True
            Game.data_filled.remove([current_cell[0], current_cell[1], i + 1])
            value_of_cell[current_cell[0]][current_cell[1]] = 0
        else:
            # print(" REMOVED BY CONSIS", i)
            Game.data_filled.remove([current_cell[0], current_cell[1], i + 1])
            value_of_cell[current_cell[0]][current_cell[1]] = 0
    return False


def column_sum(i, j):
    global Game
    global value_of_cell
    summ = 0
    cnt = 0
    can_use = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while True:
        i += 1
        if i > 8:
            break
        if isinstance(value_of_cell[i][j], tuple):
            break
        temp = value_of_cell[i][j]
        if temp == 0:
            cnt += 1
        else:
            summ += temp
            if temp in can_use:
                can_use.remove(temp)
            else:
                return -1000, -1000
    minn = 0
    maxx = 0
    for k in can_use[:cnt]:
        minn += k
    for k in can_use[-cnt:]:
        maxx += k
    return summ + minn, maxx + summ


def row_sum(i, j):
    global Game
    summ = 0
    cnt = 0
    can_use = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while True:
        j += 1
        if j > 8:
            break
        if isinstance(value_of_cell[i][j], tuple):
            break
        temp = value_of_cell[i][j]
        if temp == 0:
            cnt += 1
        else:
            summ += temp
            if temp in can_use:
                can_use.remove(temp)
            else:
                return -1000, -1000

    minn = 0
    maxx = 0
    for k in can_use[:cnt]:
        minn += k
    for k in can_use[-cnt:]:
        maxx += k
    return summ + minn, maxx + summ


def get_left_consist(i, j):
    global value_of_cell
    while True:
        j -= 1
        if isinstance(value_of_cell[i][j], tuple):
            return i, j


def get_up_consist(i, j):
    global value_of_cell
    while True:
        i -= 1
        if isinstance(value_of_cell[i][j], tuple):
            return i, j


def update_filled_sum_value(i, j):
    global Game
    global constraint_on_cell
    xi, yi = constraint_on_cell[i][j][0]
    xj, yj = constraint_on_cell[i][j][1]
    sum_min_row, sum_max_row = row_sum(xi, yi)
    sum_min_column, sum_max_column = column_sum(xj, yj)
    # print(sum_max_row, consistent_values[(xi, yi)][0], sum_min_row)
    # print(sum_max_column, consistent_values[(xj, yj)][1], sum_min_column)
    # print(' */* ')
    # print(sum_max_row >= consistent_values[(xi, yi)][0] >= sum_min_row and \
    #       sum_max_column >= consistent_values[(xj, yj)][1] >= sum_min_column
    #       )
    return sum_max_row >= value_of_cell[xi][yi][0] >= sum_min_row and \
           sum_max_column >= value_of_cell[xj][yj][1] >= sum_min_column


# def update_order_domain_values(i, j, value, order_domain_values, Game, remove):
#     xi, yi = get_up_consist(Game, i, j)
#     xj, yj = get_left_consist(Game, i, j)
#     if remove:
#         xi = xi + 1
#         while xi < 9 and [xi, yi] in Game.data_fills:
#             values = order_domain_values[(xi, yi)]
#             if value in values:
#                 values.remove(value)
#             order_domain_values[(xi, yi)] = values
#             # print("Updating order domain value of :", (xi, yi), " ::: ", order_domain_values[(xi, yi)])
#             xi = xi + 1
#
#         yj = yj + 1
#         while yj < 9 and [xj, yj] in Game.data_fills:
#             values = order_domain_values[(xj, yj)]
#             if value in values:
#                 values.remove(value)
#             order_domain_values[(xj, yj)] = values
#             # print("Updating order domain value of :", (xj, yj), " ::: ", order_domain_values[(xj, yj)])
#             yj = yj + 1
#
#     else:
#         xi = xi + 1
#         while xi < 9 and [xi, yi] in Game.data_fills:
#             values = order_domain_values[(xi, yi)]
#             if value not in values:
#                 values.append(value)
#             order_domain_values[(xi, yi)] = values
#             # print("Updating order domain value of :", (xi, yi), " ::: ", order_domain_values[(xi, yi)], " ADD *")
#             xi = xi + 1
#
#         yj = yj + 1
#         while yj < 9 and [xj, yj] in Game.data_fills:
#             values = order_domain_values[(xj, yj)]
#             if value not in values:
#                 values.append(value)
#             order_domain_values[(xj, yj)] = values
#             # print("Updating order domain value of :", (xj, yj), " ::: ", order_domain_values[(xj, yj)], "ADD *")
#             yj = yj + 1
#
#     return order_domain_values

def print_mp():
    global value_of_cell
    for i in range(9):
        for j in range(9):
            print(value_of_cell[i][j], end='\t')
        print()
    print(" ***************** ")
