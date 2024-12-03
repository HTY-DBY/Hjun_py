# %%
import os
import subprocess

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main, check_files_exist_and_non_empty_In_Other_main

# 配置参数
kraken2_save_path = GobleD().kraken2_save_path
bracken_save_path = GobleD().bracken_save_path
creat_path_In_Other_main([kraken2_save_path, bracken_save_path])
print(f'=========================================\n'
	  f'Begin: bracken ')
print(f'bracken_save_path: {bracken_save_path}')

# 检查文件是否存在且大小是否大于0


# %%
# 遍历 SRA 目录
not_down_sra = []
root_count = len([d for d in os.listdir(kraken2_save_path) if os.path.isdir(os.path.join(kraken2_save_path, d))])

i = 1
for root, dirs, files in os.walk(kraken2_save_path):
	if root == kraken2_save_path:
		continue  # 跳过根目录

	# 获取 SRA ID
	sra_id = os.path.basename(root)
	bracken_each_save_path = os.path.join(bracken_save_path, sra_id)

	if not os.path.exists(bracken_each_save_path):
		os.makedirs(bracken_each_save_path)

	# 通用参数配置
	k_report_path = os.path.join(root, 'kraken2_report.txt')
	output_path = os.path.join(bracken_each_save_path, 'bracken_result.txt')

	if check_files_exist_and_non_empty_In_Other_main([output_path]):
		print(f'{sra_id} 已经存在')
		i += 1
		continue

	cmd_common = (
		f'-d {GobleD().kraken2_db} '
		f'-i {k_report_path} '
		f'-o {output_path} '
		f'-l G '
	)

	cmd_fastp = f'bracken {cmd_common} '

	# 总共的样本数量
	# print(f'{i + 1}/{root_count} SRA ID: {sra_id}, 类型: {"SE" if is_se else "PE"}')
	print(f'执行命令: \n{cmd_fastp}')

	try:
		# 执行命令
		subprocess.run(cmd_fastp, shell=True, check=True)
		print(f'[成功] SRA ID: {sra_id} 结果保存至 {bracken_each_save_path}')
	except subprocess.CalledProcessError as e:
		print(f'[失败] SRA ID: {sra_id}, 错误信息: {e}')
		not_down_sra.append(sra_id)

	print('---------------------------------------')
	i += 1

# 打印未成功处理的 SRA IDs
if not_down_sra:
	print(f'[警告] 以下 SRA ID 处理失败：{not_down_sra}')
