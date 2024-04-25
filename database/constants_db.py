import os

MAX_LIMIT = 100
MAX_OFFSET = 10000

URL_API = ""
URL_API = URL_API.format(MAX_LIMIT, "{}", "{}")

# POSTGRES PARAMS
dbname = "anggota"
user = "postgres"
password = "admin"
host = "localhost"
port = 5432


NEW_COLUMNS = []

COLUMNS_TO_NORMALIZE = []

COLUMNS_TO_KEEP = []

DB_FIELDS = COLUMNS_TO_KEEP + COLUMNS_TO_NORMALIZE + NEW_COLUMNS