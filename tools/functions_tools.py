import ast
import json
from datetime import datetime

from langchain.tools import Tool

from database.sql_db_langchain import db
from tools.tools_constants import COLUMNS_DESCRIPTIONS


def run_query_save_results(db, query):
    """
    Runs a query on the specified database and returns the results.

    Args:
        db: The database object to run the query on.
        query: The query to be executed.

    Returns:
        A list containing the results of the query.
    """
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub]
    return res


def get_hard_query(query: str) -> str:

    kelamin_P = run_query_save_results(
        db, "SELECT COUNT(*) FROM anggota WHERE kelamin = 'P';"
    )
    
    kelamin_L = run_query_save_results(
        db, "SELECT COUNT(*) FROM anggota WHERE kelamin = 'L';"
    )
    kelamin_P_str = (
        "Jumlah total anggota berkelamin Perempuan : \n"
        + json.dumps(kelamin_P, ensure_ascii=False)
    )
    kelamin_L_str = (
        "Jumlah total anggota berkelamin Laki-laki : \n"
        + json.dumps(kelamin_L, ensure_ascii=False)
    )

    return kelamin_P_str, kelamin_L_str


def get_columns_descriptions(query: str) -> str:
    """
    Useful to get the description of the columns in the table.
    """
    return json.dumps(COLUMNS_DESCRIPTIONS)


def get_today_date(query: str) -> str:
    """
    Useful to get the date of today.
    """

    # Getting today's date in string format
    today_date_string = datetime.now().strftime("%Y-%m-%d")
    return today_date_string


def sql_agent_tools():
    tools = [
        Tool.from_function(
            func=get_hard_query,
            name="get_hard_query",
            description="""
            Useful to get hard query. A json is returned.
            """,
        ),
        Tool.from_function(
            func=get_columns_descriptions,
            name="get_columns_descriptions",
            description="""
            Useful to get the description of the columns in the table.
            """,
        ),
        Tool.from_function(
            func=get_today_date,
            name="get_today_date",
            description="""
            Useful to get the date of today.
            """,
        ),
    ]
    return tools