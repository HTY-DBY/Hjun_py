import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main

# 配置参数
sra_save_path = GobleD().sra_save_path
creat_path_In_Other_main([sra_save_path])

print(f'=========================================\n'
	  f'Begin: sra_down')
print(f'sra_path: {sra_save_path}')

# 读取数据
database_ori_SRA = pd.read_excel(GobleD().database_excel, sheet_name='SRA')

# %%
test_do = 1
column_SRA_ID = 'SRA_ID_test' if test_do else 'SRA_ID'


# 函数：下载 SRA 文件
def download_sra(sra_id, sra_save_path, row, total_rows):
	sra_file_path = os.path.join(sra_save_path, sra_id, f'{sra_id}.sra')

	# 检查文件是否存在且非空
	if check_files_exist_and_non_empty_In_Other_main([sra_file_path]):
		return f'{row + 1}/{total_rows} --- {sra_id} 已经存在'

	# 构建下载命令
	cmd_sra_down = f'"{GobleD().prefetch}" "{sra_id}" -O "{sra_save_path}" --max-size u'

	try:
		# 清除可能存在的锁文件
		lock_file = os.path.join(sra_save_path, sra_id, f'{sra_id}.sra.lock')
		if os.path.exists(lock_file):
			os.remove(lock_file)
			print(f"已删除锁文件: {lock_file}")

		# 执行下载命令
		print(f"{row + 1}/{total_rows} --- 开始下载 {sra_id}")
		subprocess.run(cmd_sra_down, shell=True, check=True)
		print(f"{row + 1}/{total_rows} --- 成功下载 {sra_id}")
	except Exception as e:
		print(f"{row + 1}/{total_rows} --- 下载失败 {sra_id}: \n{e}")

		# 如果下载失败，重试机制
		retry_count = 3
		while retry_count > 0:
			print(f"重试中: {row + 1}/{total_rows} --- {retry_count} 尝试下载 {sra_id}")
			try:
				subprocess.run(cmd_sra_down, shell=True, check=True)
				print(f"{row + 1}/{total_rows} --- 成功下载 {sra_id}")
				break
			except Exception as e:
				print(f"{row + 1}/{total_rows} --- 未知错误 {sra_id}: \n{e}")

			retry_count -= 1
			time.sleep(10)  # 等待后重试
	print('---------------------------------------')


# 多线程下载
max_threads = os.cpu_count()  # 设置线程数量
count_database_ori_SRA = len(database_ori_SRA[column_SRA_ID].dropna(how='all'))
with ThreadPoolExecutor(max_threads) as executor:
	futures = {
		executor.submit(download_sra, database_ori_SRA.loc[row, column_SRA_ID], sra_save_path, row, count_database_ori_SRA): row
		for row in range(count_database_ori_SRA)
	}

	for future in as_completed(futures):
		print(future.result())
