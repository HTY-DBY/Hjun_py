import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


def sra_to_fastq_sub(sra_file_path, fastq_each_save_path):
	# 构建获取 fastq 文件的命令
	cmd_fastq_get = f'"{GobleD().fasterq_dump}" "{sra_file_path}" --outdir "{fastq_each_save_path}" --split-3 -p -e {os.cpu_count()}'
	print(f'执行命令: \n{cmd_fastq_get}')
	subprocess.run(cmd_fastq_get, shell=True, check=True)


def sra_to_fastq_FunSRA(sra_save_path, fastq_save_path, show_exist=1):
	read_path = sra_save_path
	output_path = fastq_save_path
	creat_path_In_Other_main([output_path])  # 如果不存在，则创建

	topic_main = 'fastq_get'
	Print_pro_begin_In_Other_main(topic_main)

	Error_list = []
	total_indexs = len(os.listdir(read_path))

	# 遍历主目录下的一级子目录
	for index, root in enumerate(os.walk(read_path), start=0):
		if root[0] == read_path:
			continue  # 跳过根目录

		sra_id = os.path.basename(root[0])
		# read_each_save_path = os.path.join(read_path, sra_id)
		# output_each_save_path = os.path.join(output_path, sra_id)
		output_each_save_path = os.path.join(output_path, sra_id)  # 定义当前 SRA 文件对应的 FASTQ 输出路径

		fastq_1_file_path = os.path.join(output_each_save_path, f'{sra_id}_1.fastq')  # 当前 .fastq 文件的路径
		fastq_file_path = os.path.join(output_each_save_path, f'{sra_id}.fastq')  # 当前 .fastq 文件的路径

		if (check_files_exist_and_non_empty_In_Other_main([fastq_1_file_path]) or
				check_files_exist_and_non_empty_In_Other_main([fastq_file_path])):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			continue

		sra_file_path = os.path.join(root[0], f'{sra_id}.sra')  # 当前 .sra 文件的路径
		if not os.path.exists(sra_file_path):
			Error_list.append(sra_id)
			print(f'{sra_id}.sra 未成功下载 跳过')
			continue

		try:
			print(f'{index}/{total_indexs} SRA ID: {sra_id}')
			sra_to_fastq_sub(sra_file_path, output_each_save_path)
			print(f'{index}/{total_indexs} --- [成功]\n'
				  f'SRA ID: {sra_id} 保存至 {output_each_save_path}')
		except Exception as e:
			Error_list.append(sra_id)
			# 打印具体的错误信息
			print(f'{index}/{total_indexs} --- [失败]\n'
				  f' SRA ID: {sra_id}. 错误信息: \n{e}')

		print('---------------------------------------')

	if Error_list:
		print(f'-------------------------\n错误的:')
		for sra_id in Error_list: print(f'Error: {sra_id}')

	print(f'=========================================\n'
		  f'End: {topic_main}')

	return Error_list


if __name__ == '__main__':
	# %%
	sra_save_path = GobleD().sra_save_path
	fastq_save_path = GobleD().fastq_save_path

	Error_list = sra_to_fastq_FunSRA(sra_save_path, fastq_save_path, show_exist=1)
