import time
import random
from classCG.Goods import Goods
from goodsQRUtils.analyzeQR import decode_qrcode
from voice import loadGood_voice, loadSuccess_voice

from queue import Queue

class LoadGoods:

    def __init__(self):
        self.good_list = []
        self.target_list = []
        self.initQueue()
        self.count = 0

    def load_goods(self):
        time.sleep(1)
        start_time = time.time()
        # self.count = self.count + 1
        while True:
            infor = decode_qrcode()
            if infor:
                self.goods_queue.get()
                print(infor)
                loadSuccess_voice()
                break
            else:
                # self.count = self.count + 1
                # print("couont", self.count)
                # if self.count % 3 != 0:
                #     infor = None
                #     break
                loadGood_voice()
                print("没有读到二维码,请调整位置重新出示")
            
            random_number = random.randint(0, 10)
            if time.time() - start_time > random_number:
                # count = count - 1
            # if count % 3 != 0: 
                infor = None
                break

        if infor:       
            print("装入infor给货物")
            good = Goods(infor[0],infor[2],infor[1],infor[3],infor[4])
            self.good_list.append(good)
            # TODO 前端: 给前端发送装载的货物信息
            if self.emitter != None:
                self.emitter.loadGood(good.getGno())
        else:
            self.addGoodsQueue()

    def clearGoods(self):
        self.good_list = []
        self.target_list = []

    def initTarget(self):
        for good in self.good_list:
            # 未被送过/签收
            if good.getSigned() == False :
                # 获取目的地
                destination = good.getDestination()
                self.target_list.append(destination)

    def getTarget(self):
        return self.target_list.copy()
    
    def getGoodsList(self):
        return self.good_list.copy()
    
    def addGoods(self, good):
        # time.sleep(2)
        # loadSuccess_voice()
        self.good_list.append(good)

        # TODO 前端: 给前端发送装载的货物信息
        if self.emitter != None:
                gno = good.getGno()
                print("告知前端装货 ", gno)
                self.emitter.loadGood(gno)
        
    def setEmitter(self, emitter):
        self.emitter = emitter

    def initQueue(self):
        self.goods_queue = Queue()

        # 将预先定义的货物添加到队列中
        goods_batch1 = []
        
        # 添加货物到队列中
        for goods in goods_batch1:
            self.goods_queue.put(goods)

    # 队列中拿货物
    def addGoodsQueue(self):
        if not self.goods_queue.empty():
            good = self.goods_queue.get()
            print("队列数", self.goods_queue.qsize())
            self.good_list.append(good)
            loadSuccess_voice()
            if self.emitter != None:
                    self.emitter.loadGood(good.getGno())
        else:
            print("队列空了")
    
    
if __name__ == '__main__':

    # 装货流程
    loadGoods = LoadGoods()
    for i in range(3):
        loadGoods.load_goods()

#     # 装货流程
#     loadGoods = LoadGoods()
#     good1 = Goods("G01",(4,4),"M@gmail.com","小明","1")
#     good2 = Goods("G02",(2,3),"F@gmail.com","BO","2")
#     good3 = Goods("G03",(1,5),"J@gmail.com","JJ侠","1")
#     loadGoods.addGoods(good1)
#     loadGoods.addGoods(good2)
#     loadGoods.addGoods(good3)
#     loadGoods.initTarget()
#     target_list = loadGoods.getTarget()
#     print(target_list)