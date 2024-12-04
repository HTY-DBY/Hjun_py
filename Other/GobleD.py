import os

from Other.Other_main import get_windows_username_In_Other_main

develop = 1 if get_windows_username_In_Other_main() == '99791' else 0


# %%
class GobleD:
	def __init__(self, ):
		self.Main_Path = r"/mnt/d/hty/creat/paper/do/HJun/PY" if develop \
			else r"/mnt/c/hty/hj/Hjun_py-main"
		self.sratoolkit = r'/home/hty/ins/sratoolkit.3.1.1-ubuntu64/bin' if develop \
			else r'/home/hty/ins/sratoolkit.3.1.1-ubuntu64/bin'
		self.prefetch = os.path.join(self.sratoolkit, 'prefetch') if develop \
			else os.path.join(self.sratoolkit, 'prefetch')
		self.fasterq_dump = os.path.join(self.sratoolkit, 'fasterq-dump') if develop \
			else os.path.join(self.sratoolkit, 'fasterq-dump')

		# 数据库主路径
		self.database_path = r'/mnt/d/hty/creat/paper/do/HJun/Database' if develop \
			else r'/mnt/e/Database'

		# 具体的文件
		self.database_excel = os.path.join(self.database_path, "Database.xlsx") if develop \
			else os.path.join(self.database_path, "Database.xlsx")
		self.kraken2_db = r'/mnt/d/hty/creat/paper/do/HJun/Tool/kraken2_db' if develop \
			else r'/mnt/c/hty/hj/Tool/kraken2_db'
		# 具体的路径
		self.excel = os.path.join(self.database_path, "excel") if develop \
			else os.path.join(self.database_path, "excel")
		self.sra_save_path = os.path.join(self.database_path, "sra") if develop \
			else os.path.join(self.database_path, "sra")
		self.fastq_save_path = os.path.join(self.database_path, "fastq") if develop \
			else os.path.join(self.database_path, "fastq")
		self.fastq_better_save_path = os.path.join(self.database_path, "fastq_better") if develop \
			else os.path.join(self.database_path, "fastq_better")
		self.megahit_save_path = os.path.join(self.database_path, "megahit") if develop \
			else os.path.join(self.database_path, "megahit")
		self.kraken2_save_path = os.path.join(self.database_path, "kraken2") if develop \
			else os.path.join(self.database_path, "kraken2")
		self.bracken_save_path = os.path.join(self.database_path, "bracken") if develop \
			else os.path.join(self.database_path, "bracken")


if __name__ == '__main__':
	# 初始化对象
	GobleD = GobleD()
	pass
