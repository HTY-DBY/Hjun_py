# %%
import pandas as pd
from Other.GobleD import GobleD
from Other.Other_main import reload_modules_In_Other_main
from Pretreatment.sra_handle.Fun_sra.blast_blastn_fun import blast_makeblastdb
from Pretreatment.sra_handle.Fun_sra.bracken_fun import bracken_FunSRA
from Pretreatment.sra_handle.Fun_sra.fastp_fun import fastp_FunSRA
from Pretreatment.sra_handle.Fun_sra.fastqc_fun import fastqc_FunSRA
from Pretreatment.sra_handle.Fun_sra.kraken2_fun import kraken2_FunSRA
from Pretreatment.sra_handle.Fun_sra.pear_fun import pear_FunSRA
from Pretreatment.sra_handle.Fun_sra.seqtk_t_fasta_fun import seqtk_t_fasta_FunSRA
from Pretreatment.sra_handle.Fun_sra.sratoolkit_down_sra_fun import sra_down_FunSRA
from Pretreatment.sra_handle.Fun_sra.sratoolkit_get_fastq_fun import sra_to_fastq_FunSRA

# reload_all_modules_In_Other_main() # 重新导入模块
# 读取和配置数据
database_ori_SRA = pd.read_excel(GobleD().database_excel, sheet_name='SRA')

test_do = 1
column_SRA_ID = 'SRA_ID_test' if test_do else 'SRA_ID'
sra_need_list = database_ori_SRA[column_SRA_ID].dropna(how='all')
sra_save_path = GobleD().sra_save_path
fastq_save_path = GobleD().fastq_save_path
fastq_better_save_path = GobleD().fastq_better_save_path
kraken2_save_path = GobleD().kraken2_save_path
bracken_save_path = GobleD().bracken_save_path
pear_fastq_better_save_path = GobleD().pear_fastq_better_save_path
seqtk_t_fasta_with_pear_fastq_better = GobleD().seqtk_t_fasta_with_pear_fastq_better_save_path
# %%
se_Goble = 0
# reload_modules_In_Other_main(["Other", "Pretreatment"])

sra_down_FunSRA(sra_save_path, sra_need_list, show_exist=se_Goble, max_threads=20)
Error_list_sra_to_fastq = sra_to_fastq_FunSRA(sra_save_path, fastq_save_path, show_exist=se_Goble)
Error_list_fastp = fastp_FunSRA(fastq_save_path, fastq_better_save_path, show_exist=se_Goble, drop_old=0)
Error_list_kraken2 = kraken2_FunSRA(fastq_better_save_path, kraken2_save_path, show_exist=se_Goble)
Error_list_bracken = bracken_FunSRA(kraken2_save_path, bracken_save_path, show_exist=se_Goble)

Error_list_pear = pear_FunSRA(fastq_better_save_path, pear_fastq_better_save_path, show_exist=se_Goble)

Error = seqtk_t_fasta_FunSRA(pear_fastq_better_save_path, seqtk_t_fasta_with_pear_fastq_better,
							 read_postfix='.assembled.fastq', output_postfix='.fasta', show_exist=se_Goble)
