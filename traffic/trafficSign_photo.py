 # -*- coding: utf-8 -*

import cv2

def capture_TrafficSign():
    # 打开摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return False, None

    # 捕获一帧图像
    ret, frame = cap.read()

    # 检查帧是否成功捕获
    if not ret:
        print("无法捕获图像")
        return False, None
    
    fileName = "traffic/img/sign.jpg"
    # 保存图像文件
    cv2.imwrite(fileName, frame)

    # 关闭摄像头
    cap.release()

    print("交通标志照片已保存")
    return True, fileName
    
