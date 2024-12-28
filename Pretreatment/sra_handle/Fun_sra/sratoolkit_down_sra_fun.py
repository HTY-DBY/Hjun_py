import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# 函数：下载 SRA 文件
def download_sra_sub(sra_id, sra_save_path, index, total_indexs, show_exist):
	sra_file_path = os.path.join(sra_save_path, sra_id, f'{sra_id}.sra')

	# 检查文件是否存在且非空
	if check_files_exist_and_non_empty_In_Other_main([sra_file_path]):
		if show_exist: print(f'{index + 1}/{total_indexs} --- {sra_id} 已经存在')
		return None

	# 构建下载命令
	cmd_sra_down = f'"{GobleD().prefetch}" "{sra_id}" -O "{sra_save_path}" --max-size u'

	try:
		# 清除可能存在的锁文件
		lock_file = os.path.join(sra_save_path, sra_id, f'{sra_id}.sra.lock')
		if os.path.exists(lock_file):
			os.remove(lock_file)
			print(f"已删除锁文件: {lock_file}")

		# 执行下载命令
		print(f"{index + 1}/{total_indexs} --- 开始下载 {sra_id}")
		subprocess.run(cmd_sra_down, shell=True, check=True)
		print(f"{index + 1}/{total_indexs} --- 成功下载 {sra_id}")
	except Exception as e:
		print(f"{index + 1}/{total_indexs} --- 下载失败 {sra_id}: \n{e}")

		# 如果下载失败，重试机制
		retry_count = 3
		while retry_count > 0:
			print(f"重试中: {index + 1}/{total_indexs} --- {retry_count} 尝试下载 {sra_id}")
			try:
				subprocess.run(cmd_sra_down, shell=True, check=True)
				print(f"{index + 1}/{total_indexs} --- 成功下载 {sra_id}")
				break
			except Exception as e:
				print(f"{index + 1}/{total_indexs} --- 未知错误 {sra_id}: \n{e}")

			retry_count -= 1
			time.sleep(10)  # 等待后重试
	print('---------------------------------------')


def sra_down_FunSRA(sra_save_path, sra_need_list, show_exist=1, max_threads=20, ):
	creat_path_In_Other_main([sra_save_path])  # 如果不存在，则创建

	topic_main = 'sra_down'
	Print_pro_begin_In_Other_main(topic_main)

	# 多线程下载
	sra_need_list_num = len(sra_need_list)

	with ThreadPoolExecutor(max_threads) as executor:
		futures = {
			executor.submit(download_sra_sub, sra_need_list[index], sra_save_path, index, sra_need_list_num, show_exist): index
			for index in range(sra_need_list_num)
		}

		for future in as_completed(futures):
			if future.exception() is not None:
				print(future.result())

	print(f'=========================================\n'
		  f'End: {topic_main}')


if __name__ == '__main__':
	# %%
	sra_save_path = GobleD().sra_save_path
	sra_need_list = ['SRR28741039', 'SRR22183625', 'SRR29303764']

	sra_down_FunSRA(sra_save_path, sra_need_list, show_exist=1)
