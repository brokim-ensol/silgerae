# sqllite3를 이용하여 데이터베이스를 생성하고, 데이터를 저장하는 코드
import sqlite3
import pandas as pd
from process import pre_process


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


def read_data(conn: sqlite3.Connection = None, table_name: str = "section_one"):
    if conn is None:
        conn = sqlite3.connect("db/silgerae.db")
    df = pd.read_sql(
        sql=f"SELECT * FROM {table_name}",
        con=conn,
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


if __name__ == "__main__":
    create_table()
