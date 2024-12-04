import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import argparse

# 邮件配置信息
my_sender = '997916923@qq.com'  # 发件人邮箱账号
my_pass = 'shhsljwolyfzbfga'  # 发件人邮箱授权码
my_user = '997916923@qq.com'  # 收件人邮箱账号


def mail(content, subject):
	"""
	发送邮件
	:param content: 邮件正文
	:param subject: 邮件标题
	"""
	ret = True
	try:
		# 设置邮件内容
		msg = MIMEText(content, 'plain', 'utf-8')
		msg['From'] = formataddr(["tracy", my_sender])
		msg['To'] = formataddr(["test", my_user])
		msg['Subject'] = subject

		# 连接到 SMTP 服务器并发送邮件
		server = smtplib.SMTP_SSL("smtp.qq.com", 465)
		server.login(my_sender, my_pass)
		server.sendmail(my_sender, [my_user], msg.as_string())
		server.quit()
	except Exception as e:
		print(f"Error：{e}")
		ret = False
	return ret


if __name__ == '__main__':
	# 配置命令行参数解析
	parser = argparse.ArgumentParser(description="发送邮件脚本")
	parser.add_argument('-txt', required=True, help="邮件正文")
	parser.add_argument('-title', required=True, help="邮件标题")
	args = parser.parse_args()

	# 读取参数
	email_text = args.txt
	email_title = args.title

	# 发送邮件
	mail(email_text, email_title)
