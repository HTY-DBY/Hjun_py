import os
import subprocess

from Other.GobleD import GobleD


def creat_path_In_Other_main(creat_path):
	for path in creat_path:
		if not os.path.exists(path):
			os.makedirs(path)
			print(f"Created directory: {path}")


def check_files_exist_and_non_empty_In_Other_main(files):
	for file in files:
		if not os.path.exists(file):
			# print(f"{file} does not exist.")
			return False
		if os.path.getsize(file) == 0:
			# print(f"{file} is empty.")
			return False
	return True


def Send_email_In_Other_main(title=None, txt=None, ):
	if txt is None:
		txt = "test"
	if title is None:
		title = "test"

	cmd = f'{GobleD().windows_python} "{GobleD().send_email_script}" -txt {txt} -title {title}'

	try:
		print(f"开始 发送邮件，执行命令\n{cmd}")
		print(f'title: {title}\ntxt: {txt}')
		result = subprocess.run(cmd, shell=True, check=True)
		print("成功 发送邮件")
		if result.stderr:
			print(f"标准错误：\n{result.stderr}")
	except subprocess.CalledProcessError as e:
		print(f"脚本执行失败，错误信息：\n{e.stderr}")
