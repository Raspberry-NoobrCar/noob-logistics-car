import heapq

class Node:
    def __init__(self, position):
        self.position = position
        self.g_cost = 0  # 从起点到当前节点的实际代价
        self.h_cost = 0  # 从当前节点到终点的预计代价
        self.f_cost = 0  # g_cost + h_cost
        self.parent = None

    def __lt__(self, other):
        return self.f_cost < other.f_cost

def heuristic_cost(current_node, target_node):
    # 计算当前节点到目标节点的启发式估计值
    # 这里使用曼哈顿距离作为启发函数
    return abs(target_node.position[0] - current_node.position[0]) + abs(target_node.position[1] - current_node.position[1])

def get_neighbors(current_node, grid):
    # 获取当前节点的相邻节点
    neighbors = []
    row, col = current_node.position

    # 定义相邻节点的偏移量
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for offset in offsets:
        new_row = row + offset[0]
        new_col = col + offset[1]

        # 检查相邻节点是否在网格范围内
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            # 忽略不可通过的节点（例如障碍物）
            if grid[new_row][new_col] == 1:
                continue

            neighbor = Node((new_row, new_col))
            neighbors.append(neighbor)

    return neighbors

# A*算法取单个目标的最短路径
def a_star(grid, start, target):
    open_list = []
    closed_set = set()

    start_node = Node(start)
    target_node = Node(target)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == target_node.position:
            # 找到了最短路径
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # 反转路径

        closed_set.add(current_node.position)

        neighbors = get_neighbors(current_node, grid)
        for neighbor in neighbors:
            if neighbor.position in closed_set:
                continue

            neighbor.g_cost = current_node.g_cost + 1  # 假设每个网格代价为1
            neighbor.h_cost = heuristic_cost(neighbor, target_node)
            neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
            neighbor.parent = current_node

            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)
            else:
                # 更新节点的代价和父节点
                index = open_list.index(neighbor)
                if neighbor.g_cost < open_list[index].g_cost:
                    open_list[index].g_cost = neighbor.g_cost
                    open_list[index].parent = neighbor.parent

    # 没有找到路径
    return None

# dp计算tsp最佳路径
def path_dp(grid_map, start, target_list):
    try:
        if target_list:
            # while target_list:
            # path_list = []
            target_record = None
            path = []
            path_len = 56
            for target in target_list:
                temp_path = a_star(grid_map, start, target)
                if temp_path:
                    temp_len = len(temp_path)
                    # nearest neighbor
                    if temp_len < path_len: 
                        path_len = temp_len
                        path = temp_path
                        # path_list = temp_path
                        target_record = target
                else:
                    print("no path to this target:", target)

            # print(target_record)
            # 删除这个目标点
            target_list.remove(target_record)
            # print(target_list)
            # print(path)
            # 递归算下一个路径
            if target_list :
                next_path = path_dp(grid_map, target_record, target_list)
                path = path + next_path[1:]
                # path_list = path_list + next_path

            return path
        else:
            print("no target, must give!")
        
    except Exception as e:
        print(e)


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
    start = (0, 0)
    target_list = [(4, 4),(2,1),(5,2)]

    # path, pl = path_dp(grid, start, target_list)
    path = path_dp(grid, start, target_list)
    print(path)
    # print(pl)

