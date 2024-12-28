# %%
import os

from Other.GobleD import GobleD
from Pretreatment.sra_handle.Fun_sra.blast_blastn_fun import blast_makeblastdb

# %%
in_mdb = GobleD().blast_db_nucl_ori
dbtype_mdb = 'nucl'
out_mdb = os.path.join(GobleD().blast_db_nucl_path, "blast_db_nucl")

blast_makeblastdb(in_mdb, dbtype_mdb, out_mdb)
