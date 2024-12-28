# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%


def fastqc_sub(need_path_sub):
	# 构建获取 fastq 文件的命令
	cmd_set = f'fastqc {need_path_sub}/*.fastq -q -t {os.cpu_count()}'
	print(f'执行命令: \n{cmd_set}')
	subprocess.run(cmd_set, shell=True, check=True)


def fastqc_FunSRA(need_path, show_exist=1):
	topic_main = 'fasqc'
	Print_pro_begin_In_Other_main(topic_main)
	Error_list = []
	total_indexs = len(os.listdir(need_path))

	# 遍历主目录下的一级子目录
	for index, root in enumerate(os.walk(need_path), start=0):
		if root[0] == need_path:
			continue  # 跳过根目录

		sra_id = os.path.basename(root[0])
		need_path_sub = root[0]

		fastq_1_file_path = os.path.join(root[0], f'{sra_id}_1_fastqc.html')  # 当前 .fastq 文件的路径
		fastq_file_path = os.path.join(root[0], f'{sra_id}_fastqc.html')  # 当前 .fastq 文件的路径
		if check_files_exist_and_non_empty_In_Other_main([fastq_1_file_path]) or check_files_exist_and_non_empty_In_Other_main([fastq_file_path]):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经 {topic_main}')
			continue

		try:
			print(f'{index}/{total_indexs} --- SRA ID: {sra_id}')
			fastqc_sub(need_path_sub)
			print(f'{index}/{total_indexs} --- [成功], SRA ID: {sra_id}')
		except Exception as e:
			print(f'[失败] SRA ID: {sra_id}. 错误信息: \n{e}')
			Error_list.append(sra_id)

	if Error_list:
		print(f'-------------------------\n错误的:')
		for sra_id in Error_list: print(f'Error: {sra_id}')

	print(f'=========================================\n'
		  f'End: {topic_main}')


if __name__ == '__main__':
	# %%
	need_path = GobleD().fastq_save_path

	fastqc_FunSRA(need_path, show_exist=1)
