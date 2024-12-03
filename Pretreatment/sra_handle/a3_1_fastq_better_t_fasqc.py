# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main

# 配置参数
# fastq_save_path = GobleD().fastq_save_path
fastq_better_save_path = GobleD().fastq_better_save_path
creat_path_In_Other_main([fastq_better_save_path])

print(f'=========================================\n'
	  f'Begin: fastq_better_t_fasqc')
print(f'fastq_better_save_path: {fastq_better_save_path}')

# %%
not_down_sra = []
root_count = len(os.listdir(fastq_better_save_path))

i = 0
# 遍历主目录下的一级子目录
for root, dirs, files in os.walk(fastq_better_save_path):
	if root == fastq_better_save_path:
		continue  # 跳过根目录

	sra_id = os.path.basename(root)
	fastq_each_save_path = os.path.join(fastq_better_save_path, sra_id)  # 定义当前 SRA 文件对应的 FASTQ 输出路径

	fastq_1_file_path = os.path.join(fastq_each_save_path, f'{sra_id}_1_fastqc.html')  # 当前 .fastq 文件的路径
	fastq_file_path = os.path.join(fastq_each_save_path, f'{sra_id}_fastqc.html')  # 当前 .fastq 文件的路径
	if os.path.exists(fastq_1_file_path) or os.path.exists(fastq_file_path):
		# 检查是否已存在 .fastq 文件
		print(f'{sra_id} 已经存在')
		i += 1
		continue

	# 构建获取 fastq 文件的命令
	cmd_fastq_get = f'fastqc {fastq_each_save_path}/*.fastq -q -t {os.cpu_count()}'
	# --extract

	print(f'{i + 1}/{root_count}  处理 SRA ID: {sra_id}')
	print(f'执行命令: \n{cmd_fastq_get}')

	try:
		# 执行命令
		subprocess.run(cmd_fastq_get, shell=True, check=True)
		print(f'[成功] SRA ID: {sra_id} 保存至 {fastq_each_save_path}')
	except subprocess.CalledProcessError as e:
		# 打印具体的错误信息
		print(f'[失败] SRA ID: {sra_id}. 错误信息: {e}')

	print('---------------------------------------')
	i += 1

if not_down_sra:
	print(f'-------------------------\n错误的:')
	for sra_id in not_down_sra:
		print(f'{sra_id}.sra 未成功下载')
