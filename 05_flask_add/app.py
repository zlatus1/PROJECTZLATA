
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

from db import DEFAULT_DB_PATH, fetch_all_tasks, initialize_database, insert_task

app = Flask(__name__)
app.config["SECRET_KEY"] = "projectzlata-local-coursework-key"
initialize_database(DEFAULT_DB_PATH)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Название задачи не может быть пустым.", "error")
        elif len(title) > 160:
            flash("Название задачи должно быть не длиннее 160 символов.", "error")
        else:
            try:
                insert_task(title, DEFAULT_DB_PATH)
                flash("Задача добавлена.", "success")
            except sqlite3.Error:
                flash("Не удалось сохранить задачу.", "error")
        return redirect(url_for("index"), code=303)

    return render_template("index.html", items=fetch_all_tasks(DEFAULT_DB_PATH))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
