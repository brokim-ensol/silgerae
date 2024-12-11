# app.py
from flask import Flask, session, render_template, redirect, url_for
import os
from crawl import crawl
from process import pre_process
from pathlib import Path
from db import insert_data, read_data, create_table, save_dataframe
import pandas as pd
import json
import plotly
import plotly.express as px

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

        # rm latest_file using pathlib
        latest_file.unlink(missing_ok=True)

        msg1 = save_dataframe(df1, table_name="section_one")
        msg = save_dataframe(df, table_name="yangjae")

        if msg1 and msg:
            return f"df1: {msg1}, df: {msg}"
        elif msg1:
            return f"df1: {msg1}"
        elif msg:
            return f"df: {msg}"
        else:
            return redirect(url_for("show"))

    else:
        return "Failed to crawl data!"


@app.route("/show")
def show():
    df1 = read_data(table_name="section_one")
    df = read_data(table_name="yangjae")
    # df1의 updated_at 컬럼을 기준으로 최근 1주일 데이터만 가져온다.
    df1.sort_values(by="계약날짜", ascending=False, inplace=True)
    df.sort_values(by="계약날짜", ascending=False, inplace=True)

    df1 = df1.loc[:20, :]
    df = df.loc[:20, :]

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


@app.route("/graph/<endpoint>")
def graph(endpoint):
    if endpoint == "section_one":
        return gm("section_one")
    elif endpoint == "yangjae":
        return gm("yangjae")
    else:
        return "Invalid endpoint"


@app.route("/graph")
def index():

    return render_template("graph.html")


def gm(table_name="section_one"):
    # st = yf.Ticker(stock)

    # Create a line graph
    # df = st.history(period=(period), interval=interval)
    df = read_data(table_name=table_name)
    df = df[["계약날짜", "대지면적평당가격", "거래금액"]]
    # df=df.reset_index()
    # df.columns = ['Date-Time']+list(df.columns[1:])
    max_y = df["대지면적평당가격"].max()
    min_y = df["대지면적평당가격"].min()
    dev_y = max_y - min_y
    margin = dev_y * 0.05
    max_y = max_y + margin
    min_y = min_y - margin
    fig = px.scatter(
        df,
        x="계약날짜",
        y="대지면적평당가격",
        hover_data=("거래금액"),
        range_y=(min_y, max_y),
        template="seaborn",
        size="거래금액",
    )
    fig.add_hline(y=7230, line_width=2, line_dash="dash", line_color="blue")

    # Create a JSON representation of the graph
    graphJSON = fig.to_json()  # json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
