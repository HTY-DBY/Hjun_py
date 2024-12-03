# %%
import os
import subprocess

import pandas as pd

from Other.GobleD import GobleD
from Other.Other_main import creat_path_In_Other_main

# 配置参数
sra_save_path = GobleD().sra_save_path
creat_path_In_Other_main([sra_save_path])

print(f'=========================================\n'
	  f'Begin: sra_down')
print(f'sra_path: {sra_save_path}')

# 读取数据
database_ori_SRA = pd.read_excel(GobleD().database_excel, sheet_name='SRA')

# %%
test_do = 1
column_SRA_ID = 'SRA_ID_test' if test_do else 'SRA_ID'

for row in range(len(database_ori_SRA[column_SRA_ID].dropna(how='all'))):
	sra_id = database_ori_SRA.loc[row, column_SRA_ID]
	size_mb = database_ori_SRA.loc[row, 'Size (Mb)']

	sra_file_path = os.path.join(sra_save_path, sra_id, f'{sra_id}.sra')

	# 检查是否已存在
	if os.path.exists(sra_file_path):
		print(f'{sra_id} 已经存在')
		continue

	# 构建命令
	# 下载 sra
	cmd_sra_down = f'"{GobleD().prefetch}" "{sra_id}" -O "{sra_save_path}" --max-size u'
	print(f'开始下载 {sra_id} --- {row + 1}/{len(database_ori_SRA)}')

	try:
		# 执行下载命令
		subprocess.run(cmd_sra_down, shell=True, check=True)
		print(f'成功下载 {sra_id}')
	except subprocess.CalledProcessError as e:
		print(f'下载失败 {sra_id}: {e}')
