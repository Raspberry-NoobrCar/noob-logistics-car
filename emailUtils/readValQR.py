import cv2
from pyzbar.pyzbar import decode
import time

#验证取件码
def read_valQRode():
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    # 获取开始时间
    start_time = time.time()
    # 循环读取帧
    while True:
        # 读取一帧图像
        ret, frame = cap.read()

        # 判断是否成功读取帧
        if not ret:
            continue

        # 解码二维码
        qrcode = decode(frame)

        # 判断是否识别到二维码
        if len(qrcode) > 0:
            data = qrcode[0].data.decode("utf-8")
            
        # 判断是否超过
        if time.time() - start_time > 5:
            data = False
            break
            
#         # 显示图像
#         cv2.imshow("frame", frame)

#         # 按下"q"键退出循环
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

    # 返回是否识别到二维码的Boolean值
    return data

if __name__ == "__main__":
    print(read_valQRode())
    