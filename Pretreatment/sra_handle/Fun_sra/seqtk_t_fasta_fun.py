# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%


def seqtk_t_fasta_sub(read_each_save_path_files, output_each_save_path_files):
	for file_read_now, file_output_now in zip(read_each_save_path_files, output_each_save_path_files):
		cmd_set = f'seqtk seq -a "{file_read_now}" > "{file_output_now}"'
		print(f'执行命令: \n{cmd_set}')
		subprocess.run(cmd_set, shell=True, check=True)


def seqtk_t_fasta_FunSRA(read_path, output_path, show_exist=1, read_postfix='.fastq', output_postfix='.fasta'):
	creat_path_In_Other_main([output_path])

	topic_main = 'seqtk_t_fasta'
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
		creat_path_In_Other_main([output_each_save_path])

		is_se = os.path.exists(os.path.join(read_each_save_path, f'{sra_id}{read_postfix}'))
		read_each_save_path_files = [
			os.path.join(read_each_save_path, f'{sra_id}{suffix}{read_postfix}')
			for suffix in ([''] if is_se else ['_1', '_2'])
		]
		output_each_save_path_files = [
			os.path.join(output_each_save_path, f'{sra_id}{suffix}{output_postfix}')
			for suffix in ([''] if is_se else ['_1', '_2'])
		]

		if check_files_exist_and_non_empty_In_Other_main(output_each_save_path_files):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			continue
		print(f'{index}/{total_indexs} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')

		try:
			seqtk_t_fasta_sub(read_each_save_path_files, output_each_save_path_files)
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
	fastq_better_save_path = GobleD().fastq_better_save_path
	Error_list = seqtk_t_fasta_FunSRA(fastq_better_save_path, fastq_better_save_path, show_exist=1)
