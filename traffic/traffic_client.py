import requests


def  traffic_client():
    
        # 设置请求的URL
        url = "http://192.168.50.75:5000/detect_image"
       
        
        # 读取本地图片文件
        image_path = "traffic/img/sign.jpg"
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # 构建请求参数，将图片文件作为字典中的值
        files = {'image': image_data}
        
        # 发送POST请求
        response = requests.post(url, files=files)
        
        # 检查请求的响应状态码
        if response.status_code == 200:
            print("Image uploaded successfully!")
            # 获取服务器端返回的JSON数据
            result_dict = response.json()
            # 提取检测结果
            detection_result = result_dict["result"]
            # 处理检测结果，例如打印或显示在界面上
            print("Detection result:", detection_result)
            return detection_result
        else:
            print("Image upload failed.")
            
if  __name__=="__main__":
        traffic_client()
        