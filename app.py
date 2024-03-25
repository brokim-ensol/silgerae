# app.py
from flask import Flask, session, render_template
import os
from crawl import crawl
from process import pre_process
from pathlib import Path
from db import insert_data, read_data, create_table, save_dataframe
import pandas as pd

app = Flask(__name__)

# app secret key
app.secret_key = "brokim"


@app.route("/")
def hello_world():  # put application's code here
    try:
        create_table()
        return "DB created!"
    except:
        return "Hello World!"


@app.route("/crawl")
def do_crawl():
    latest_file = crawl()
    session["latest_file"] = str(latest_file)

    if latest_file:
        df1, df = pre_process(Path(latest_file))

        msg1 = save_dataframe(df1, table_name="section_one")
        msg = save_dataframe(df, table_name="yangjae")

        if msg1 and msg:
            return f"df1: {msg1}, df: {msg}"
        elif msg1:
            return f"df1: {msg1}"
        elif msg:
            return f"df: {msg}"
        else:
            return "Success to crawl and save data!"

    else:
        return "Failed to crawl data!"


@app.route("/show")
def show():
    df1 = read_data(table_name="section_one")
    df = read_data(table_name="yangjae")
    # df1의 updated_at 컬럼을 기준으로 최근 1주일 데이터만 가져온다.
    df1 = df1[df1["updated_at"] > pd.to_datetime("now") - pd.DateOffset(weeks=1)]
    df = df[df["updated_at"] > pd.to_datetime("now") - pd.DateOffset(weeks=1)]

    return render_template(
        "show.html",
        tables=[
            df1.to_html(
                classes="table table-bordered table-intel",
                table_id="table1",
                border=0,
                index=False,
            ),
            df.to_html(
                classes="table table-bordered table-intel",
                table_id="table2",
                border=0,
                index=False,
            ),
        ],
        titles=["na", "1구역", "양재2동 전체"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
