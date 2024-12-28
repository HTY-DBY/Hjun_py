# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%


def bracken_sub(read_each_save_path, output_each_save_path):
	creat_path_In_Other_main([output_each_save_path])
	k_report_path = os.path.join(read_each_save_path, 'kraken2_report.txt')
	bracken_file_output_path = os.path.join(output_each_save_path, 'bracken_result.txt')
	cmd_common = (
		f'-d {GobleD().kraken2_db} '
		f'-i {k_report_path} '
		f'-o {bracken_file_output_path} '
		f'-l G '
	)

	cmd_set = f'bracken {cmd_common} '

	print(f'执行命令: \n{cmd_set}')
	subprocess.run(cmd_set, shell=True, check=True)


def bracken_FunSRA(kraken2_save_path, bracken_save_path, show_exist=1):
	read_path = kraken2_save_path
	output_path = bracken_save_path
	creat_path_In_Other_main([output_path])

	topic_main = 'bracken'
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

		bracken_file_output_path = os.path.join(output_each_save_path, 'bracken_result.txt')
		if check_files_exist_and_non_empty_In_Other_main([bracken_file_output_path]):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			continue

		print(f'{index}/{total_indexs} --- SRA ID: {sra_id}')

		try:
			bracken_sub(read_each_save_path, output_each_save_path)
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
	kraken2_save_path = GobleD().kraken2_save_path
	bracken_save_path = GobleD().bracken_save_path
	Error_list = bracken_FunSRA(kraken2_save_path, bracken_save_path, show_exist=1)
