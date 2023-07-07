# 解析货物二维码
import cv2
from pyzbar.pyzbar import decode


def val_qrcode():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

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
            temp = tuple(data.split("/"))
            location = temp[2]
            x = int(location[1])
            y = int(location[3])
            local_tuple = (x, y)
            found = (temp[0], temp[1], local_tuple, temp[3])
            break
        else:
            found = False

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
    print(val_qrcode())
