from classCG.Car import Car
from classCG.Goods import Goods
from LoadGoods import LoadGoods
from RunMap import RunMap
from voice import loading_voice, loadFinished_voice, loadAgain_voice
import time

def run(emitter = None):
    
    # 示例数据
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    # 起点
    start = (0, 0)
    # 终点
    end = (0, 0)
    # 起始朝向 / 朝左
    selfTurnVector = (0,1)

    runCar = Car()
    runCar.initCarSetup()

    loadGoods = LoadGoods()
    loadGoods.setEmitter(emitter)
    goods_list = []

    runMap = RunMap()
    runMap.setEmitter(emitter)
    runMap.setEnd(end)
       
    # -------------------

#     try:
#         # 开始移动
#         while True:
            
#             target_list_copy = target_list.copy()
#             goods_list_copy = goods_list.copy()
#             runMap = RunMap(runCar, start, selfTurnVector, grid, goods_list_copy, target_list_copy)
#             runMap.initPath()
#             runMap.followTrafficRules()
            
#     except ValueError as e: 
#         print(str(e)) 
#     except Exception as e:  # 其他异常情况
#         print(str(e)) 

    while True:
        # 装货流程
        if goods_list == []:
            print("装货过程")
            # loading_voice()     # 装货提示音

            for _ in range(4):
                loadGoods.load_goods()

            # loadFinished_voice()

            goods_list = loadGoods.getGoodsList()
            # 初始化 目的地list
            loadGoods.initTarget()
            target_list = loadGoods.getTarget()
        
        # if runMap.end

        target_list_copy = target_list.copy()
        goods_list_copy = goods_list.copy()
        print("目的地 ", target_list_copy)
        print("包裹数量 ", len(goods_list_copy))
        # 装载信息
        runMap.setInfo(runCar, start, selfTurnVector, grid, goods_list_copy, target_list_copy)
        # 规划路线
        runMap.initPath()
        # 开始移动
        flag = runMap.pathFllowWalk()
        
        if flag == 504:    # 障碍物
            print("障碍物重新获取信息")
            start, selfTurnVector, grid, goods_list, target_list = runMap.getInformation()
        elif flag == 305:  # 返回终点
            print("正在获取信息并准备返回终点")
            start, selfTurnVector, grid, _, _ = runMap.getInformation()
            # 这里不清货
            target_list = [end]
        elif flag == 406:   # 已经返回终点
            loadAgain_voice()
            start, selfTurnVector, grid, _, _ = runMap.getInformation()
            # 清空货物 / 卸货
            loadGoods.clearGoods()
            goods_list = []
            target_list = []
        elif flag == 701:    # 禁止前行
            print("禁止前行重新获取信息")
            start, selfTurnVector, grid, goods_list, target_list = runMap.getInformation()
        elif flag == 909:   # 没有可达目的地的路径
            print("没有可达目的地的路径")
            if runMap.emitter != None:
                # 故障求救
                runMap.emitter.handleError("没有可达目的地的路径")
            break
        elif flag == 910:
            print("终点返回错误")
        elif flag == 110:
            print("错误的转向指令")
            if runMap.emitter != None:
                # 故障求救
                runMap.emitter.handleError("错误的转向指令")
            break


if __name__ == '__main__':

    run()