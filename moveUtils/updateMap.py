
def addObstacle(grid_map, position):
    x_element = position[1]
    y_element = position[0]

    try:
        grid_map[y_element][x_element] = 1
        return grid_map
    except Exception as e:
        print(e)

def resetZeroMap(grid_map):
    y_len = len(grid_map)
    x_len = len(grid_map[0])

    if x_len and y_len:
        zero_list = [[0 for _ in range(x_len)] for _ in range(y_len)]
        return zero_list

if __name__ == '__main__':
    # 地图示例
    grid = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    # new_map = resetZeroMap(grid)
    new_map = addObstacle(grid, (0,0))
    print(new_map)