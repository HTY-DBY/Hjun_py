# %%
import os
import shutil
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main, Print_pro_begin_In_Other_main


# %%


def fastp_sub(fastq_each_save_path, fastq_better_each_save_path, is_se, sra_id):
	creat_path_In_Other_main([fastq_better_each_save_path])
	cmd_common = (
		f'--cut_front --cut_tail '  # 去除 reads 的前端和尾部接头，确保无多余序列，这里采用默认值。
		f'--length_required 50 '  # 只保留长度大于等于 50 bp 的 reads，过滤掉过短的 reads。
		f'--qualified_quality_phred 20 '  # 确保保留的碱基质量值（Phred score）大于等于 20。
		f'--unqualified_percent_limit 40 '  # 默认40，丢弃含有超过 40% 低质量碱基（质量值 <20）的 reads。
		# f'--n_base_limit 6 '  # 丢弃含有超过 6 个 N 碱基（未确定碱基）的 reads。
		# f'--compression 6 '  # 压缩输出文件，压缩级别为 6，平衡文件大小与处理速度。
		f'--html "{os.path.join(fastq_better_each_save_path, f"{sra_id}.html")}" '  # 生成 HTML 格式的质量控制报告，路径为每个 SRA ID 的子目录。
		f'--json "{os.path.join(fastq_better_each_save_path, f"{sra_id}.json")}"'  # 生成 JSON 格式的质量控制报告，路径同上。
	)

	# fastp uses up to 16 threads although you specified 20
	threads_set = min(16, os.cpu_count())

	# 判断单端（SE）还是双端（PE）
	if is_se:
		in1 = os.path.join(fastq_each_save_path, f'{sra_id}.fastq')
		out1 = os.path.join(fastq_better_each_save_path, f'{sra_id}.fastq')
		cmd_set = f'fastp -i "{in1}" -o "{out1}" --thread {threads_set} {cmd_common}'
	else:
		in1 = os.path.join(fastq_each_save_path, f'{sra_id}_1.fastq')
		in2 = os.path.join(fastq_each_save_path, f'{sra_id}_2.fastq')
		out1 = os.path.join(fastq_better_each_save_path, f'{sra_id}_1.fastq')
		out2 = os.path.join(fastq_better_each_save_path, f'{sra_id}_2.fastq')
		cmd_set = (
			f'fastp -i "{in1}" -I "{in2}" -o "{out1}" -O "{out2}" '
			f'--thread {threads_set} {cmd_common}'
		)

	print(f'执行命令: \n{cmd_set}')
	subprocess.run(cmd_set, shell=True, check=True)


def fastp_FunSRA(fastq_save_path, fastq_better_save_path, show_exist=1, drop_old=0):
	read_path = fastq_save_path
	output_path = fastq_better_save_path

	if drop_old:
		print("\033[31m注意，将删除旧的 .fastq 文件\033[0m")

	creat_path_In_Other_main([fastq_better_save_path])

	topic_main = 'fastp_better'
	Print_pro_begin_In_Other_main(topic_main)
	# 遍历目录
	Error_list = []
	total_indexs = len(os.listdir(fastq_save_path))

	for index, root in enumerate(os.walk(fastq_save_path), start=0):
		if root[0] == fastq_save_path:
			continue  # 跳过根目录

		sra_id = os.path.basename(root[0])
		read_each_save_path = os.path.join(read_path, sra_id)
		output_each_save_path = os.path.join(output_path, sra_id)

		fastq_1_file_path = os.path.join(output_each_save_path, f'{sra_id}_1.fastq')  # 当前 .fastq 文件的路径
		fastq_file_path = os.path.join(output_each_save_path, f'{sra_id}.fastq')  # 当前 .fastq 文件的路径
		if (check_files_exist_and_non_empty_In_Other_main([fastq_1_file_path]) or
				check_files_exist_and_non_empty_In_Other_main([fastq_file_path])):
			# 检查是否已存在 .fastq 文件
			if show_exist: print(f'{index}/{total_indexs} --- {sra_id} 已经存在')
			if drop_old: shutil.rmtree(root[0])
			continue

		is_se = os.path.exists(os.path.join(fastq_save_path, sra_id, f'{sra_id}.fastq'))
		print(f'{index}/{total_indexs} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')

		try:
			# 执行命令
			fastp_sub(read_each_save_path, output_each_save_path, is_se, sra_id)
			print(f'{index}/{total_indexs} --- [成功] SRA ID: {sra_id} 结果保存至 {output_each_save_path}')
			if drop_old: shutil.rmtree(root[0])
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
	fastq_save_path = GobleD().fastq_save_path
	fastq_better_save_path = GobleD().fastq_better_save_path
	Error_list = fastp_FunSRA(fastq_save_path, fastq_better_save_path, show_exist=1)
