import time

# The moving direction of the car

# 向量乘
def multiplicationVector(a,b):
    y_result = a[0] * b[0]
    x_result = a[1] * b[1]

    return y_result + x_result

# 向量叉乘
def crossproductVector(a,b):
    result1 = a[0] * b[1]
    result2 = a[1] * b[0]

    return result2 - result1

# 向量减法
def subtractionVector(a,b):
    y_result = a[0] - b[0]
    x_result = a[1] - b[1]

    return (y_result,x_result)

# 向量减法
def addVector(a,b):
    y_result = a[0] + b[0]
    x_result = a[1] + b[1]

    return (y_result,x_result)

# 下一步的方向
def nextDirection(selfTurnVector, nextVector):
    """
        规定:
            右:1
            左:2
            前:3
            后:4
            error:0
    """

    # 向量内积
    resultNum = multiplicationVector(selfTurnVector, nextVector)
    # 如果垂直
    if resultNum == 0:
        # 向量外积
        resultNum_cross = crossproductVector(selfTurnVector, nextVector)
        # 积正为右
        if resultNum_cross == 1:
            # print("turn right")
            return 1
        elif resultNum_cross == -1:
            # print("turn left")
            return 2
    elif resultNum == 1:    # 不垂直 方向一致
        # print("continue")
        return 3
    elif resultNum == -1:   # 不垂直 方向相反
        # print("back")
        return 4
    else:
        # print("error")
        return 0



if __name__ == '__main__':

    # 示例数据
    grid = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    target_list = [(4, 4),(2,1),(5,2)]
    selfTurnVector = (0,1)

    # -----------

    # 获取路径
    target_list_copy = target_list.copy()
    path,= path_dp(grid, start, target_list_copy)
    print(path)

    # 开始移动
    if start == path[0]:
        path = path[1:]
        for next_yx in path :
            nextVector = subtractionVector(next_yx, start)
            nextDirection(selfTurnVector, nextVector)
            selfTurnVector = nextVector
            start = next_yx
            time.sleep(3)
            if next_yx in target_list:
                print(next_yx,"到达！")
                # print("到达！")
    else:
        print("start not in path")

