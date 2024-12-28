# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%

def blast_makeblastdb(in_mdb, dbtype_mdb, out_mdb):
	cmd_set = f'makeblastdb -in "{in_mdb}" -dbtype "{dbtype_mdb}" -out "{out_mdb}"'
	print(f'执行命令: \n{cmd_set}')
	subprocess.run(cmd_set, shell=True, check=True)


def blast_sub(read_each_save_path, output_each_save_path, sra_id):
	creat_path_In_Other_main([output_each_save_path])
	query_file = os.path.join(read_each_save_path, f'{sra_id}.fasta')
	output_file = os.path.join(output_each_save_path, 'blast_result.txt')
	db_path = os.path.join(GobleD().blast_db_nucl_path, "blast_db_nucl")
	cmd_common = (
		f'-db {db_path} '
		f'-num_threads {os.cpu_count()} '
		f'-task megablast '
		f'-outfmt 6 '
		f'-query {query_file} '
		f'-out {output_file} '
	)
	cmd_set = f'blastn {cmd_common}'
	print(f'执行命令: \n{cmd_set}')
	subprocess.run(cmd_set, shell=True, check=True)


def blast_FunSRA(fasta_need_path, blast_save_path, show_exist=1):
	read_path = fasta_need_path
	output_path = blast_save_path
	creat_path_In_Other_main([output_path])

	topic_main = 'blast'
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

		blast_file_path = os.path.join(output_each_save_path, 'blast_result.txt')
		if check_files_exist_and_non_empty_In_Other_main([blast_file_path]):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			continue

		print(f'{index}/{total_indexs} SRA ID: {sra_id}')

		try:
			blast_sub(read_each_save_path, output_each_save_path, sra_id)
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
	seqtk_t_fasta_with_pear_fastq_better_save_path = GobleD().seqtk_t_fasta_with_pear_fastq_better_save_path
	blast_pear_fastq_better_save_path = GobleD().blast_pear_fastq_better_save_path
	Error_list = blast_FunSRA(seqtk_t_fasta_with_pear_fastq_better_save_path, blast_pear_fastq_better_save_path, show_exist=1)
