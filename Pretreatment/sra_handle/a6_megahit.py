# %%
import os
import shutil
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main

# 配置参数
fastq_better_save_path = GobleD().fastq_better_save_path
megahit_save_path = GobleD().megahit_save_path
creat_path_In_Other_main([fastq_better_save_path, megahit_save_path])
print(f'=========================================\n'
	  f'Begin: megahit')
print(f'megahit_save_path: {megahit_save_path}')

# %%
# 遍历 SRA 目录
not_down_sra = []
root_count = len([d for d in os.listdir(fastq_better_save_path) if os.path.isdir(os.path.join(fastq_better_save_path, d))])

i = 0
for root, dirs, files in os.walk(fastq_better_save_path):
	if root == fastq_better_save_path:
		continue  # 跳过根目录

	# 获取 SRA ID
	sra_id = os.path.basename(root)
	megahit_each_save_path = os.path.join(megahit_save_path, sra_id)

	# 如果目录存在，删除该目录
	if os.path.exists(megahit_each_save_path):
		final_contigs_fa = os.path.join(megahit_each_save_path, 'final.contigs.fa')
		if check_files_exist_and_non_empty_In_Other_main([final_contigs_fa]):
			print(f'{sra_id} 已经存在')
			i += 1
			continue
		else:
			shutil.rmtree(megahit_each_save_path)

	# 通用参数配置
	cmd_common = (
		f'-o {megahit_each_save_path} '  # 指定 MEGAHIT 输出目录，确保每个样本有独立的保存路径
		f'-t {os.cpu_count()} '  # 动态设置线程数，使用系统可用的 CPU 核心数（默认值是系统可用的所有线程数）
		'--k-step 10 '  # 设置 k-mer 的递增步长为 10（默认值是 10，用于控制k-mer的步长）
		'--k-min 27 '  # 设置最小 k-mer 为 27（默认值是 27，决定拼接的最小k-mer长度）
		'--min-contig-len 200 '  # 过滤掉长度小于 200 bp 的 contig（默认值是 200，过滤掉短的拼接片段）
	)

	# 判断单端（SE）还是双端（PE）
	is_se = os.path.exists(os.path.join(root, f'{sra_id}.fastq'))
	if is_se:
		in1 = os.path.join(root, f'{sra_id}.fastq')
		cmd_fastp = f'megahit -r "{in1}"  {cmd_common}'
	else:
		in1 = os.path.join(root, f'{sra_id}_1.fastq')
		in2 = os.path.join(root, f'{sra_id}_2.fastq')
		cmd_fastp = (
			f'megahit -1 "{in1}" -2 "{in2}" {cmd_common}'
		)
	# 总共的样本数量
	print(f'{i + 1}/{root_count} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')
	print(f'执行命令: \n{cmd_fastp}')

	try:
		# 执行命令
		subprocess.run(cmd_fastp, shell=True, check=True)
		print(f'[成功] SRA ID: {sra_id} 结果保存至 {megahit_each_save_path}')
	except subprocess.CalledProcessError as e:
		print(f'[失败] SRA ID: {sra_id}, 错误信息: {e}')
		not_down_sra.append(sra_id)

	print('---------------------------------------')
	i += 1

# 打印未成功处理的 SRA IDs
if not_down_sra:
	print(f'[警告] 以下 SRA ID 处理失败：{not_down_sra}')
