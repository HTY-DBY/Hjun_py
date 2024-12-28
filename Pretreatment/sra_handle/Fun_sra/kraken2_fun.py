# %%
import os
import shutil
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%


def kraken2_sub(read_each_save_path, output_each_save_path, is_se, sra_id):
	kraken2_file_report_path = os.path.join(output_each_save_path, 'kraken2_report.txt')
	kraken2_file_output_path = os.path.join(output_each_save_path, 'kraken2_output.txt')
	cmd_common = (
		f'--db {GobleD().kraken2_db} '
		f'--threads {os.cpu_count()} '
		f'--report {kraken2_file_report_path} '
		f'--output {kraken2_file_output_path} '
		f'--memory-mapping '
	)

	if is_se:
		in1 = os.path.join(read_each_save_path, f'{sra_id}.fastq')
		cmd_set = f'kraken2 {in1} --quick {cmd_common} {in1}'
	else:
		in1 = os.path.join(read_each_save_path, f'{sra_id}_1.fastq')
		in2 = os.path.join(read_each_save_path, f'{sra_id}_2.fastq')
		cmd_set = f'kraken2 {in1} {in2} --quick {cmd_common} --paired'

	print(f'执行命令: \n{cmd_set}')
	subprocess.run(cmd_set, shell=True, check=True)


def kraken2_FunSRA(fastq_better_save_path, kraken2_save_path, show_exist=1):
	read_path = fastq_better_save_path
	output_path = kraken2_save_path
	creat_path_In_Other_main([output_path])

	topic_main = 'kraken2'
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

		kraken2_file_report_path = os.path.join(output_each_save_path, 'kraken2_report.txt')
		kraken2_file_output_path = os.path.join(output_each_save_path, 'kraken2_output.txt')
		if check_files_exist_and_non_empty_In_Other_main([kraken2_file_report_path, kraken2_file_output_path]):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			continue

		is_se = os.path.exists(os.path.join(read_each_save_path, f'{sra_id}.fastq'))
		print(f'{index}/{total_indexs} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')

		try:
			kraken2_sub(read_each_save_path, output_each_save_path, is_se, sra_id)
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
	fastq_better_save_path = GobleD().fastq_better_save_path
	kraken2_save_path = GobleD().kraken2_save_path
	Error_list = kraken2_FunSRA(fastq_better_save_path, kraken2_save_path, show_exist=1)
