import os
import subprocess


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


def get_windows_username_In_Other_main():
	try:
		result = subprocess.check_output('cmd.exe /c "echo %USERNAME%"', shell=True, text=True)
		return result.strip()
	except Exception as e:
		return None
