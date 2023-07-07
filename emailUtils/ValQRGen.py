import qrcode

def generateValQrcode(Gno):
    # 创建二维码对象并设置数据
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # 创建QR码对象并接受给定设置数据
    data = Gno

    qr.add_data(data)
    qr.make(fit=True)

    # 创建QR码图像并保存为PNG文件
    img = qr.make_image(fill_color="black", back_color="white")
    fileName =  "emailPhoto/ValQR/" + Gno + ".jpg"
    img.save(fileName)
    return fileName

if __name__ =="__main__":
    generateValQrcode("G01")