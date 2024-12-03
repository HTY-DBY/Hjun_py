# %%
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# %%
# 发送者和接收者的邮箱地址
sender_email = "hty2dby@gmail.com"
receiver_email = "997916923@qq.com"
password = "460805asdA"

# 邮件内容
subject = "Test Email"
body = "This is a test email sent from Python using Gmail."

# 创建邮件对象
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    # 连接到 Gmail 的 SMTP 服务器
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # 启动 TLS 加密
    server.login(sender_email, password)  # 登录 Gmail 邮箱
    text = msg.as_string()

    # 发送邮件
    server.sendmail(sender_email, receiver_email, text)
    print("邮件发送成功!")

except Exception as e:
    print(f"发送邮件失败: {e}")

finally:
    server.quit()  # 退出服务器连接
