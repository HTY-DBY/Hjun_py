import importlib
import os
import shutil
import subprocess

import sys

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

	cmd = f'{GobleD().windows_python} "{GobleD().send_email_script}" -txt "{txt}" -title "{title}"'

	try:
		print(f"开始 发送邮件，执行命令\n{cmd}")
		print(f'title: {title}\ntxt: {txt}')
		result = subprocess.run(cmd, shell=True, check=True)
		print("成功 发送邮件")
		if result.stderr:
			print(f"标准错误：\n{result.stderr}")
	except subprocess.CalledProcessError as e:
		print(f"脚本执行失败，错误信息：\n{e.stderr}")


def Fix_space_name_path_In_Other_main(path):
	# 处理文件名中的空格
	for root, dirs, files in os.walk(path):
		if root == path:
			continue  # 跳过根目录

		if ' ' in root:
			new_filename = root.replace(' ', '_')
			new_path = os.path.join(root, new_filename)

			# 重命名文件
			os.rename(root, new_path)
			print(f'文件名修改: {root} -> {new_path}')


def Print_pro_begin_In_Other_main(topic_main):
	print(f'-----------------------------------------\n'
		  f'\033[32mBegin: {topic_main}\033[0m'
		  f'\n=========================================')


def reload_modules_In_Other_main(modules_to_reload):
	for module_name in modules_to_reload:
		if module_name in sys.modules:  # 确保模块已被导入
			importlib.reload(sys.modules[module_name])
		else:
			print(f"模块 {module_name} 未被导入，跳过。")


def del_directory_In_Other_main(directory):
	if os.path.exists(directory) and os.path.isdir(directory):
		# 如果目录为空，使用 os.rmdir() 删除
		if not os.listdir(directory):
			os.rmdir(directory)
		# print(f"空目录 '{directory}' 已删除。")
		else:
			# 如果目录非空，使用 shutil.rmtree() 删除
			shutil.rmtree(directory)
		# print(f"非空目录 '{directory}' 已删除。")
