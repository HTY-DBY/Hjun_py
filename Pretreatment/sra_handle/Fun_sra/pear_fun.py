# %%
import os
import shutil
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%


def pear_sub(read_each_save_path, output_each_save_path, is_se, sra_id):
	creat_path_In_Other_main([output_each_save_path])
	if is_se:
		file = os.path.join(read_each_save_path, f'{sra_id}.fastq')
		output_file = os.path.join(output_each_save_path, f'{sra_id}.assembled.fastq')
		shutil.copy(file, output_file)
		print('SE 数据 复制完成')
	else:
		file_1 = os.path.join(read_each_save_path, f'{sra_id}_1.fastq')
		file_2 = os.path.join(read_each_save_path, f'{sra_id}_2.fastq')
		output_file = os.path.join(output_each_save_path, f'{sra_id}')

		cmd_set = f'pear -f "{file_1}" -r "{file_2}" -o "{output_file}" -j {os.cpu_count()}'
		print(f'执行命令: \n{cmd_set}')
		subprocess.run(cmd_set, shell=True, check=True)


def pear_FunSRA(fastq_save_path, pear_save_path, show_exist=1):
	read_path = fastq_save_path
	output_path = pear_save_path
	creat_path_In_Other_main([output_path])

	topic_main = 'pear'
	Print_pro_begin_In_Other_main(topic_main)
	# 遍历目录
	Error_list = []
	total_indexs = len(os.listdir(read_path))

	for index, root in enumerate(os.walk(read_path), start=0):
		if root[0] == read_path:
			continue  # 跳过根目录

		sra_id = os.path.basename(root[0])
		read_each_save_path = os.path.join(read_path, sra_id)
		output_each_save_path = os.path.join(output_path, sra_id)

		file = os.path.join(output_each_save_path, f'{sra_id}.assembled.fastq')
		file_1 = os.path.join(output_each_save_path, f'{sra_id}_1.assembled.fastq')
		if (check_files_exist_and_non_empty_In_Other_main([file, ]) or
				check_files_exist_and_non_empty_In_Other_main([file_1, ])):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			continue

		is_se = os.path.exists(os.path.join(read_each_save_path, f'{sra_id}.fastq'))
		print(f'{index}/{total_indexs} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')

		try:
			pear_sub(read_each_save_path, output_each_save_path, is_se, sra_id)
			print(f'{index}/{total_indexs} --- [成功] SRA ID: {sra_id} 结果保存至 {output_each_save_path}')
		except Exception as e:
			print(f'{index}/{total_indexs} --- [失败] SRA ID: {sra_id}, 错误信息: \n{e}')
			Error_list.append(sra_id)

		print('---------------------------------------')

	if Error_list:
		print(f'-------------------------\n错误的:')
		for sra_id in Error_list: print(f'Error: {sra_id}')

	print(f'=========================================\n'
		  f'End: {topic_main}')

	return Error_list


if __name__ == '__main__':
	# %%
	fastq_save_path = GobleD().fastq_better_save_path
	pear_save_path = GobleD().pear_fastq_better_save_path
	Error_list = pear_FunSRA(fastq_save_path, pear_save_path, show_exist=1)
