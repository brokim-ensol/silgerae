# sqllite3를 이용하여 데이터베이스를 생성하고, 데이터를 저장하는 코드
import sqlite3
import pandas as pd
from process import pre_process
import random
import string


# 데이터베이스 생성
def create_table():
    conn = sqlite3.connect("db/silgerae.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE section_one(
            번지 text NOT NULL,
            본번 text,
            부번 text,
            건물명 text,
            층 integer NOT NULL,
            전용면적 real NOT NULL,
            대지면적 real NOT NULL,
            계약날짜 text,
            거래금액 integer,
            건축년도 integer,
            대지면적평당가격 interger,
            양재2동 integer,
            일구역 integer,
            updated_at text,
            PRIMARY KEY (번지, 층, 전용면적, 대지면적)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE yangjae(
            번지 text NOT NULL,
            본번 text,
            부번 text,
            건물명 text,
            층 integer NOT NULL,
            전용면적 real NOT NULL,
            대지면적 real NOT NULL,
            계약날짜 text,
            거래금액 integer,
            건축년도 integer,
            대지면적평당가격 interger,
            양재2동 integer,
            일구역 integer,
            updated_at text,
            PRIMARY KEY (번지, 층, 전용면적, 대지면적)
        )
    """
    )

    conn.commit()
    conn.close()


# 데이터베이스 insert
def insert_data(
    df: pd.DataFrame, con: sqlite3.Connection = None, table_name: str = "section_one"
):
    if con is None:
        con = sqlite3.connect("db/silgerae.db")
    # df["계약날짜"] = df["계약날짜"].dt.strftime("%Y-%m-%d")
    df.to_sql(table_name, con, if_exists="append", index=False)


def read_data(con: sqlite3.Connection = None, table_name: str = "section_one"):
    if con is None:
        con = sqlite3.connect("db/silgerae.db")
    df = pd.read_sql(
        sql=f"SELECT * FROM {table_name}",
        con=con,
        dtype={
            "번지": "str",
            "본번": "str",
            "부번": "str",
            "건물명": "str",
            "층": "int",
            "전용면적": "float",
            "대지면적": "float",
            "계약날짜": "str",
            "거래금액": "int",
            "건축년도": "int",
            "대지면적평당가격": "int",
            "양재2동": "bool",
            "일구역": "bool",
            "updated_at": "str",
        },
    )
    df["계약날짜"] = pd.to_datetime(df["계약날짜"], format="%Y-%m-%d")
    df["updated_at"] = pd.to_datetime(df["updated_at"], format="%Y-%m-%d %H:%M:%S")
    return df


def table_column_names(
    con: sqlite3.Connection = None, table_name: str = "section_one"
) -> str:
    """
    Get column names from database table_name
    Parameters
    ----------
    table_name : str
        name of the table
    Returns
    -------
    str
        names of columns as a string so we can interpolate into the SQL queries
    """

    if con is None:
        con = sqlite3.connect("db/silgerae.db")

    cursor = con.cursor()

    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
    rows = cursor.execute(query)
    dirty_names = [i[0] for i in rows]
    clean_names = "`" + "`, `".join(map(str, dirty_names)) + "`"
    return clean_names


def insert_conflict_ignore(
    df: pd.DataFrame,
    con: sqlite3.Connection = None,
    table_name: str = "section_one",
    index: bool = False,
):
    """
    Saves dataframe to the MySQL database with 'INSERT IGNORE' query.

    First it uses pandas.to_sql to save to temporary table.
    After that it uses SQL to transfer the data to destination table, matching the columns.
    Destination table needs to exist already.
    Final step is deleting the temporary table.
    Parameters
    ----------
    df : pd.DataFrame
        dataframe to save
    table : str
        destination table name
    """
    # generate random table name for concurrent writing
    if con is None:
        con = sqlite3.connect("db/silgerae.db")

    temp_table = "".join(random.choice(string.ascii_letters) for i in range(10))
    try:
        df.to_sql(table_name, con, index=index)
        columns = table_column_names(con=con, table_name=table_name)
        insert_query = f"INSERT IGNORE INTO {table_name}({columns}) SELECT {columns} FROM `{temp_table}`"
        con.execute(insert_query)
    except Exception as e:
        print(e)

    # drop temp table
    drop_query = f"DROP TABLE IF EXISTS `{temp_table}`"
    con.execute(drop_query)


def save_dataframe(df: pd.DataFrame, table_name: str):
    """
    Save dataframe to the database.
    Index is saved if it has name. If it's None it will not be saved.
    It implements INSERT IGNORE when inserting rows into the MySQL table.
    Table needs to exist before.
    Arguments:
        df {pd.DataFrame} -- dataframe to save
        table {str} -- name of the db table
    """
    if df.index.name is None:
        save_index = False
    else:
        save_index = True

    insert_conflict_ignore(df=df, table_name=table_name, index=save_index)


if __name__ == "__main__":
    create_table()
