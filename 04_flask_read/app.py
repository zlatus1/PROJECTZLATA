
from flask import Flask, render_template

from db import DEFAULT_DB_PATH, fetch_all_tasks, initialize_database

app = Flask(__name__)
initialize_database(DEFAULT_DB_PATH)


@app.get("/")
def index():
    return render_template("index.html", items=fetch_all_tasks(DEFAULT_DB_PATH))


@app.get("/about")
def about():
    return "Практика 4: задачи читаются из SQLite и отображаются через Jinja2."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
