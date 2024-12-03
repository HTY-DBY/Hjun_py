# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main

# 配置参数
fastq_better_save_path = GobleD().fastq_better_save_path
kraken2_save_path = GobleD().kraken2_save_path
creat_path_In_Other_main([fastq_better_save_path, kraken2_save_path])
print(f'=========================================\n'
	  f'Begin: kraken2')
print(f'kraken2_save_path: {kraken2_save_path}')

# 检查文件是否存在且大小是否大于0


# %%
# 遍历 SRA 目录
not_down_sra = []
root_count = len([d for d in os.listdir(fastq_better_save_path) if os.path.isdir(os.path.join(fastq_better_save_path, d))])

i = 1
for root, dirs, files in os.walk(fastq_better_save_path):
	if root == fastq_better_save_path:
		continue  # 跳过根目录

	# 获取 SRA ID
	sra_id = os.path.basename(root)
	kraken2_each_save_path = os.path.join(kraken2_save_path, sra_id)

	if not os.path.exists(kraken2_each_save_path):
		os.makedirs(kraken2_each_save_path)

	# 通用参数配置
	report_path = os.path.join(kraken2_each_save_path, 'kraken2_report.txt')
	output_path = os.path.join(kraken2_each_save_path, 'kraken2_output.txt')

	# 判断两个文件
	if check_files_exist_and_non_empty_In_Other_main([report_path, output_path]):
		print(f'{sra_id} 已经存在')
		i += 1
		continue

	cmd_common = (
		f'--db {GobleD().kraken2_db} '
		f'--threads {os.cpu_count()} '
		f'--report {report_path} '
		f'--output {output_path} '
		f'--memory-mapping '
	)

	# 判断单端（SE）还是双端（PE）
	is_se = os.path.exists(os.path.join(root, f'{sra_id}.fastq'))
	if is_se:
		in1 = os.path.join(root, f'{sra_id}.fastq')
		cmd_fastp = f'kraken2 {in1} --quick {cmd_common} {in1}'
	else:
		in1 = os.path.join(root, f'{sra_id}_1.fastq')
		in2 = os.path.join(root, f'{sra_id}_2.fastq')
		cmd_fastp = f'kraken2 {in1} {in2} --quick {cmd_common} --paired'
	# 总共的样本数量
	print(f'{i + 1}/{root_count} 执行命令: \n{cmd_fastp}')

	try:
		# 执行命令
		subprocess.run(cmd_fastp, shell=True, check=True)
		print(f'[成功] SRA ID: {sra_id} 结果保存至 {kraken2_each_save_path}')
	except subprocess.CalledProcessError as e:
		print(f'[失败] SRA ID: {sra_id}, 错误信息: {e}')
		not_down_sra.append(sra_id)

	print('---------------------------------------')
	i += 1

# 打印未成功处理的 SRA IDs
if not_down_sra:
	print(f'[警告] 以下 SRA ID 处理失败：{not_down_sra}')
