# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main

# 配置参数
fastq_save_path = GobleD().fastq_save_path
fastq_better_save_path = GobleD().fastq_better_save_path
creat_path_In_Other_main([fastq_save_path, fastq_better_save_path])

print(f'=========================================\n'
	  f'Begin: fastp_better')
print(f'fastq_better_save_path: {fastq_better_save_path}')

# %%
# 遍历 SRA 目录
not_down_sra = []
root_count = len(os.listdir(fastq_save_path))

i = 0
# 遍历主目录下的一级子目录
for root, dirs, files in os.walk(fastq_save_path):
	if root == fastq_save_path:
		continue  # 跳过根目录

	# 获取 SRA ID
	sra_id = os.path.basename(root)

	fastq_better_each_save_path = os.path.join(fastq_better_save_path, sra_id)

	# 如果保存路径不存在，则创建
	os.makedirs(fastq_better_each_save_path, exist_ok=True)

	fastq_1_file_path = os.path.join(fastq_better_each_save_path, f'{sra_id}_1.fastq')  # 当前 .fastq 文件的路径
	fastq_file_path = os.path.join(fastq_better_each_save_path, f'{sra_id}.fastq')  # 当前 .fastq 文件的路径
	if os.path.exists(fastq_1_file_path) or os.path.exists(fastq_file_path):
		# 检查是否已存在 .fastq 文件
		print(f'{sra_id} 已经存在')
		i += 1
		continue

	# 通用参数配置
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

	# 判断单端（SE）还是双端（PE）
	is_se = os.path.exists(os.path.join(fastq_save_path, sra_id, f'{sra_id}.fastq'))
	if is_se:
		in1 = os.path.join(fastq_save_path, sra_id, f'{sra_id}.fastq')
		out1 = os.path.join(fastq_better_each_save_path, f'{sra_id}.fastq')
		cmd_fastp = f'fastp -i "{in1}" -o "{out1}" --thread {os.cpu_count()} {cmd_common}'
	else:
		in1 = os.path.join(fastq_save_path, sra_id, f'{sra_id}_1.fastq')
		in2 = os.path.join(fastq_save_path, sra_id, f'{sra_id}_2.fastq')
		out1 = os.path.join(fastq_better_each_save_path, f'{sra_id}_1.fastq')
		out2 = os.path.join(fastq_better_each_save_path, f'{sra_id}_2.fastq')
		cmd_fastp = (
			f'fastp -i "{in1}" -I "{in2}" -o "{out1}" -O "{out2}" '
			f'--thread {os.cpu_count()} {cmd_common}'
		)

	print(f'{i + 1}/{root_count} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')
	print(f'执行命令: \n{cmd_fastp}')

	try:
		# 执行命令
		subprocess.run(cmd_fastp, shell=True, check=True)
		print(f'[成功] SRA ID: {sra_id} 结果保存至 {fastq_better_each_save_path}')
	except subprocess.CalledProcessError as e:
		print(f'[失败] SRA ID: {sra_id}, 错误信息: {e}')
		not_down_sra.append(sra_id)

	print('---------------------------------------')
	i += 1

# 打印未成功处理的 SRA IDs
if not_down_sra:
	print(f'[警告] 以下 SRA ID 处理失败：{not_down_sra}')
