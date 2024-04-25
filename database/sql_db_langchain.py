import os

from langchain.sql_database import SQLDatabase
from .constants_db import port, password, user, host, dbname


url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
# TABLE_NAME = "komunitas_anggota_jatim.anggota"

db = SQLDatabase.from_uri(
    url,
    schema="komunitas_anggota", #if required
    include_tables=['anggota'],
    sample_rows_in_table_info=1,
)
print(db)