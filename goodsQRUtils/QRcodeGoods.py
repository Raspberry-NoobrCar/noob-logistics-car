import qrcode

# 生成货物二维码

""" 规定:
    GoodsNum:货物单号
    email:邮箱地址
    address:目的地坐标 (y,x)给出
    name:收件人姓名
    receivingMothd:接收方式 1为寄存 2为本人签收

"""


def generateQrcode(GoodsNum, email, address, name, receivingMothd):
    # 创建二维码对象并设置数据
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # GoodsNum = "GOODS1"
    # address = "(1,1)"

    data = GoodsNum + "/" + email + "/" + address + "/" + name + "/" + receivingMothd 
    # 二维码的数据
    qr.add_data(data)
    qr.make(fit=True)

    # 生成二维码图像
    image = qr.make_image(fill_color="black", back_color="white")
    fileName =  "goodsQRPhoto/" + GoodsNum + ".jpg"
    # 保存二维码图像
    image.save(fileName)

    return image


if __name__ == "__main__":
     print(1 + 1)
                        
