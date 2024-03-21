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

    styles = [dict(selector="tr", props=[("class", "table-info")])]

    if latest_file:
        df1 = pre_process(latest_file)

        return render_template(
            "show.html",
            tables=[
                df1.to_html(
                    classes="table table-bordered table-intel",
                    table_id="table",
                    border=0,
                    index=False,
                )
            ],
            titles=["na", "1. 1구역 평당 대지권 가격순"],
        )

    else:
        df1 = pre_process()

        return render_template(
            "show.html",
            tables=[
                df1.to_html(
                    classes="table table-bordered table-intel",
                    table_id="table",
                    border=0,
                    index=False,
                )
            ],
            titles=["na", "1. 1구역 평당 대지권 가격순"],
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
