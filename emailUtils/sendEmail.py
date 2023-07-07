import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def generateTime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M")
    return formatted_datetime


def generateBody(name, address, time):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif;background-color:white;text-align: center;">
    
    <h1 style="color:brown;text-align: center;">送货到达提醒</h1>
    <hr style=" height: 1px;">
    
    <h2 style="color:#8a6d3b;text-align: center;">您好，您的货物已经送达</h2>
    
    <h2 style="color:#8a6d3b;text-align: center;">请及时进行取件，超时未取将送回快递站</h2>
    <p style="font-size:15px;text-align: center;font-weight: bold; ">Name:{name}</p>
    <p style="font-size:15px;text-align: center;font-weight: bold; ">Address:{address}</p>
    <p style="font-size:15px;text-align: center;font-weight: bold; ">Arrive Time:{time}</p>
    <button style="display: inline-block;
                       padding: 10px 20px;
                       font-size: 16px;
                       font-weight: bold;
                       text-align: center;
                       text-decoration: none;
                       background-color: #4CAF50;
                       color: #FFFFFF;
                       border: none;
                       border-radius: 5px;
                       cursor: pointer;
                       transition: background-color 0.3s;">我知道了</button>
        
    
    <footer style="text-align:center; font-size:.8rem">Copyright @ present noob-delivery </footer>
    </body>
    <br>
    </html>
"""


def send_mail(to, subject, name, address, attachment_path):
    mail_host = os.environ.get("MAIL_HOST")
    mail_user = os.environ.get("MAIL_USER")
    mail_pass = os.environ.get("MAIL_PASS")

    me = f"{mail_user}<{mail_user}>"
    body = generateBody(name, address, generateTime())

    # 创建 MIMEMultipart 对象
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = me
    msg["To"] = ",".join(to)  # 将收件人列表转换为逗号分隔的字符串

    # 添加文本内容
    text_part = MIMEText(body, "html", "utf-8")
    msg.attach(text_part)

    # 添加附件
    if attachment_path:
        with open(attachment_path, "rb") as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(attachment_path),
            )
            msg.attach(attachment)

    try:
        s = smtplib.SMTP_SSL(mail_host)
        s.connect(mail_host, "465")
        s.login(mail_user, mail_pass)
        s.sendmail(me, to, msg.as_string())
        s.close()
        return True
    except Exception as err:
        print(err)
        return False



if __name__ == "__main__":
    email = ["TTT@gmail.com"]  # 将收件人的邮箱地址放入列表中
    name = "fjy"
    address = "unknown"
    attachment_path = "img/delivery.png"  # 替换为附件的实际路径
    send_mail(email, "ArriveMessage", name, address, attachment_path)
