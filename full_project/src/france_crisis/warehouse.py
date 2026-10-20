"""Optional DuckDB warehouse and Parquet exports."""
from pathlib import Path
import re
import pandas as pd

def build_warehouse(data_dir: Path=Path('data'), db_path: Path=Path('data/france_crisis.duckdb')) -> dict:
    try: import duckdb
    except ImportError as exc: raise RuntimeError('Install duckdb to build the analytical warehouse') from exc
    data_dir=Path(data_dir); db_path=Path(db_path); db_path.parent.mkdir(parents=True,exist_ok=True)
    parquet=data_dir/'analytical_parquet'; parquet.mkdir(parents=True,exist_ok=True)
    con=duckdb.connect(str(db_path)); loaded=[]
    try:
        for path in sorted((data_dir/'processed').glob('*.csv')):
            table=re.sub(r'[^a-zA-Z0-9_]','_',path.stem); frame=pd.read_csv(path); con.register('_frame',frame)
            con.execute(f'CREATE OR REPLACE TABLE "{table}" AS SELECT * FROM _frame')
            out=(parquet/f'{table}.parquet').resolve().as_posix().replace("'","''")
            con.execute(f'COPY "{table}" TO \'{out}\' (FORMAT PARQUET)'); con.unregister('_frame'); loaded.append(table)
    finally: con.close()
    return {'database_path':str(db_path),'parquet_directory':str(parquet),'tables':loaded}
