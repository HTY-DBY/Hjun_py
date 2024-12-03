# %%
import os

import pandas as pd

from Other.GobleD import GobleD

# %%
bracken_save_path = GobleD().bracken_save_path

all_results = pd.DataFrame()

for root, dirs, files in os.walk(bracken_save_path):
	if root == bracken_save_path:
		continue  # 跳过根目录
	sra_id = os.path.basename(root)

	# 读取 bracken_result.txt 文件
	bracken_result_all = pd.read_csv(os.path.join(root, 'bracken_result.txt'), sep='\t')

	# 选取 'name' 和 'fraction_total_reads' 列
	bracken_result = bracken_result_all[['name', 'fraction_total_reads']].set_index('name').T
	bracken_result.index = [sra_id]

	all_results = pd.concat([all_results, bracken_result], axis=0)

all_results.index.name = 'SRA_ID'
all_results.to_csv(os.path.join(GobleD().excel, 'Genus_in_sra.csv'))

if __name__ == '__main__':
	pass
