from classCG.Car import Car
from moveUtils.aStar_dp import * 
from moveUtils.carMoveDirection import *
from emailUtils.goods_photo import capture_photo
from emailUtils.sendEmail import send_mail
from emailUtils.ValQRGen import generateValQrcode
from emailUtils.readValQR import read_valQRode
from traffic.traffic_client import traffic_client
from traffic.trafficSign_photo import capture_TrafficSign
from voice import *
import time

# 运输过程

class RunMap:

    def __init__(self):
        self.good_list = []
        self.target_list = []
        self.returnFlag = False
    
    def setInfo(self, car, start, startTurnVector, gridMap, good_list, target_list):
        self.runCar = car
        self.start = start
        self.turnVector = startTurnVector
        self.gridMap = gridMap
        self.good_list = good_list
        self.target_list = target_list

    # 重新规划路径
    def setPath(self):
        # 目的地列表备份
        target_list_copy = self.target_list.copy()
        # 获取规划好的路径
        self.path = path_dp(self.gridMap, self.start, target_list_copy)

    def testPath(self):
        try:
            if not self.start == self.path[0]:
                raise ValueError("start not in path")  # 抛出路径错误
            else:
                print("start: ",self.start)
                print("path: ",self.path)
        except Exception as e:  # 其他异常情况
            print(str(e)) 
        
    def getPath(self):
        if self.path:
            return self.path.copy()
        
    def initPath(self):
        self.setPath()
        self.testPath()
    
    def setEmitter(self, emitter):
        self.emitter = emitter

    def setEnd(self,end):
        self.end = end

    def setReturnFlag(self,Rflag):
        self.returnFlag = Rflag
        
    def addObstacle(self, position):
        x_element = position[1]
        y_element = position[0]

        try:
            self.gridMap[y_element][x_element] = 1
        except Exception as e:
            print(e)

    # 按照路径行走
    def pathFllowWalk(self):
        # start = path_list[0]
        
        if not self.path:
            return 909
        if self.emitter != None:
            print("告知前端当前路径")
            # print(self.path)
            self.emitter.setPath(self.path)

        # path 坐标list
        path_list = self.path[1:]

        for next_yx in path_list :
            # 获取转向
            nextVector = subtractionVector(next_yx, self.start)
            numDirection = nextDirection(self.turnVector, nextVector)
            print("方向", numDirection)

            # 十字路口
            flag_coordinatePoints = False

            if numDirection == 3:   # 向前一步
                # 加速跑一下
                self.runCar.run(15,20)
                time.sleep(0.5)
            elif numDirection == 1: # 向右一步
                self.runCar.run(10,12)
                time.sleep(0.3)
                self.runCar.spin_right(15, 15)
                time.sleep(0.7)
            elif numDirection == 2:    # 向左一步
                self.runCar.run(12,15)
                time.sleep(0.3)
                self.runCar.spin_left(14, 13)
                time.sleep(1.1)
            elif numDirection == 4:   # 向后一步
                self.runCar.spin_left(25, 20)   # 掉头
                time.sleep(1.9)
            else:
                return 1100

            # 调整轨道 
            # 其实只要他break出来了 就是停下了
            flag_coordinatePoints = self.runCar.lineWalk()

            # 到达坐标点
            if flag_coordinatePoints:
                # 更新自身朝向
                self.turnVector = nextVector
                # 更新自身坐标
                self.start = next_yx
                print("到达坐标点  ", next_yx)

                # 新的坐标点是目的地
                if next_yx in self.target_list:

                    print("目的地 ", next_yx, " 到达！")
                    if self.emitter != None:
                        self.emitter.handleMove({ "action": "arrive", "xy": next_yx})

                    if self.returnFlag == False:
                        # 到达送货目的地 检查货物 发送邮件 / 验证二维码
                        self.checkGoods(next_yx)

                    # 到达后删除目的地
                    self.target_list.remove(next_yx)

                    print("目的地更新 ", self.target_list)

                    # 目的地空了还没返回 
                    if not len(self.target_list) and self.returnFlag == False:
                        # 终点返回 语音播报
                        self.setReturnFlag(True)
                        deliveryFinished()
                        return 305    # 返回终点标识
                    elif not len(self.target_list) and self.returnFlag == True:     
                        if next_yx == self.end:      # 到达点是终点
                            self.setReturnFlag(False)   # 将准备返回flag置空
                            # self.returnFlag = False  
                            return 406
                        else:
                            return 910

                # 如果是普通的点
                else:
                    if self.emitter != None:
                        self.emitter.handleMove({ "action": "move", "xy": next_yx})

                    label_TrafficSigns = []

                    capture_TrafficSign()
                    label_TrafficSigns = traffic_client()
                    print("len_label_TrafficSigns", label_TrafficSigns)
                    # 遇到交通标志
                    if label_TrafficSigns and len(label_TrafficSigns) != 0:
                        
                        # 按照交通规则运动
                        print("识别到交通标志", label_TrafficSigns)
                        num_TrafficSigns = self.followTrafficRules(label_TrafficSigns[0])

                        # 禁止前行 退出
                        if num_TrafficSigns == 701:
                            return 701
                    
                    # 如果没有遇到交通标志 检测障碍物
                    else:
                        flag_Obstacle = False
                        flag_Obstacle = self.runCar.tackleDetection()

                        if flag_Obstacle:
                            print("一次检测: ",flag_Obstacle)
                            # 二次检测 出现障碍，后退，左转，前进；
                            flag_secondary = self.runCar.secondary_Detection()
                            if flag_secondary:
                                print("二次检测状态: ",self.runCar.secondary_Detection())
                                self.runCar.back_Turnaround()                                
                                print("来向避退")


                            # 停下避障
                            else:
                                # 障碍物坐标
                                obstacle_yx = addVector(self.start, self.turnVector)
                                # 更新地图
                                self.addObstacle(obstacle_yx)
                                # 播放障碍物提示
                                tackle_voice()
                                print("前方障碍物 坐标", obstacle_yx)
                                if self.emitter != None:
                                    self.emitter.setBarrier({ "xy": obstacle_yx })
                            
                                return 504 # 返回障碍物标识
                        
                        else:
                            print("没有任何检测结果")
                            # 前进一下
                            self.runCar.run(15,18)
                            time.sleep(0.3)
                               

    # 到达目的地 检查货物
    def checkGoods(self, destination):
        for good in self.good_list:
            # 目的地相同 且 未被送过/签收
            if destination == good.getDestination() and good.getSigned() == False :
                email_address = good.getEmail()
                recipientName = good.getRecipientName()
                gno = good.getGno()
                print("单号",gno)
                print("接收方式",good.getReceivingMothd())
                if good.getReceivingMothd() == "1": # 接收方式是 寄存
                    # 拍照
                    photo_flag, fileName = capture_photo(gno)
                    # print(photo_flag)
                    # 发送邮件
                    if photo_flag:
                        print("发送寄存邮件")
                        send_mail(email_address, "ArriveMessage_已寄存", recipientName, destination, fileName)
                    else:
                        print("发送寄存无图邮件")
                        send_mail(email_address, "ArriveMessage", recipientName, destination, "")
                    # 播音及时签收
                    delivery_voice()
                    checkFlag = False

                elif good.getReceivingMothd() == "2": # 接收方式是 本人签收
                    # 发送验证二维码
                    QRpath = generateValQrcode(gno)
                    send_mail(email_address, "ArriveMessage_验证码", recipientName, destination, QRpath)
                    # 语音播报出示二维码
                    scanQR_voice()
                    # 验证二维码
                    checkFlag = self.checkValQR(gno)

                if self.emitter != None and checkFlag:
                    print("告知前端卸货 ", gno)
                    self.emitter.unLoadGood(gno)   

                # 标记为送过了
                good.setSigned()
        
    # 记得在终点清空 货物list
    
    def checkValQR(self,gno):  
        # 获取开始时间
        start_time = time.time()
        while True:
            infor = read_valQRode()
            if infor == gno:
                signIn_voice()
                return True
            elif infor:
                # 二维码不匹配
                notMatch_voice()
            else:
                loadGood_voice()
                print("没有读到二维码,请调整位置重新出示")

            # 判断是否超过
            if time.time() - start_time > 60:
                timeout_voice()
                return False


    def followTrafficRules(self, label_TrafficSigns):
        if label_TrafficSigns:
            print("标志标签 ",label_TrafficSigns)
            sign_yx = addVector(self.start, self.turnVector)
            if not self.emitter == None:
                self.emitter.setTrafficSign({ "type": label_TrafficSigns, "xy": sign_yx})
            if label_TrafficSigns == "p":  # 禁止前行
                # 禁止前行的语音
                forbid_voice()
                # 禁止前行的坐标
                # Psign_yx = addVector(self.start, self.turnVector)
                # 更新地图
                print("禁止前行坐标 ", sign_yx)
                self.addObstacle(sign_yx)
                return 701

            elif label_TrafficSigns == "school_stop":  # 人行道/学生通道
                # 人行道的语音
                pedestrianCrossing_voice()
                self.runCar.brake()
                time.sleep(5)
                # 重新启动的语音
                rebooting_voice()
                return 702

            elif label_TrafficSigns == "turn_around":  # 掉头
                # 测试用
                self.runCar.spin_left(25, 20)   # 掉头
                time.sleep(1.9)
                # 更新自身朝向
                # 更新自身坐标
                
            elif label_TrafficSigns == "turn_left":  # 左转
                # 测试用
                self.runCar.spin_left(14, 13)
                time.sleep(1.1)
            elif label_TrafficSigns == "turn_right":  # 右转
                # 测试用
                self.runCar.spin_right(15, 15)
                time.sleep(0.7)

    # return existing information when stop walking
    def getInformation(self):
        # 返回当前坐标 
        # 自身朝向
        # 更新后的地图
        # 剩余的货物
        # 剩余的目的地 

        return self.start, self.turnVector, self.gridMap,self.good_list, self.target_list