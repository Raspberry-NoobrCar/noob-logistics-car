import cv2
from pyzbar.pyzbar import decode
import time

def decode_qrcode():
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
            parts = data.split("/")
            # "a" "b" "c"
            if len(parts) == 3:
                text = parts[0:]
                x, y = map(int, parts[1:])
                found = (tuple(text), (x, y))
            elif len(parts) == 1:
                found = (data,)
            else:
                found = False
        else:
            found = False
            
        # 判断是否超过
        if time.time() - start_time > 15:
            found = False
            break

        # 显示图像
        cv2.imshow("frame", frame)

        # 按下"q"键退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

    # 返回是否识别到二维码的Boolean值
    return found

if __name__ == "__main__":
    print(decode_qrcode())
    