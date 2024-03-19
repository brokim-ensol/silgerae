# app.py
from flask import Flask, session, render_template
import os
from crawl import crawl
from process import pre_process
from pathlib import Path

app = Flask(__name__)

# app secret key
app.secret_key = "brokim"


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/crawl")
def do_crawl():
    latest_file = crawl()
    session["latest_file"] = str(latest_file)
    if latest_file:
        return f"success {latest_file.name}"
    else:
        return "Nothing"


@app.route("/show")
def show():
    latest_file_str = session.get("latest_file", None)
    # convert string to Path object
    try:
        latest_file = Path(latest_file_str)
    except:
        latest_file = None

    if latest_file:
        df_high, df_large, df_latest, df_expensive = pre_process(latest_file)

        return render_template(
            "show.html",
            tables=[
                df_high.head(10).to_html(classes="type1"),
                df_large.head(10).to_html(classes="type2"),
                df_latest.head(10).to_html(classes="type1"),
                df_expensive.head(10).to_html(classes="type2"),
            ],
            titles=[
                "na",
                "1. 1구역 평당 대지권 가격순",
                "2. 1구역 대지면적 25 m2 이상",
                "3. 1구역 최신 거래순",
                "4. 양재2동 7억 이상",
            ],
        )

    else:
        df_high, df_large, df_latest, df_expensive = pre_process()

        return render_template(
            "show.html",
            tables=[
                df_high.head(10).to_html(classes="type1"),
                df_large.head(10).to_html(classes="type2"),
                df_latest.head(10).to_html(classes="type1"),
                df_expensive.head(10).to_html(classes="type2"),
            ],
            titles=[
                "na",
                "1. 1구역 평당 대지권 가격순",
                "2. 1구역 대지면적 25 m2 이상",
                "3. 1구역 최신 거래순",
                "4. 양재2동 7억 이상",
            ],
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
