
from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "Hello, Flask! PROJECTZLATA работает."


@app.get("/about")
def about():
    return "Это учебный список задач на Flask. Практическая работа №3."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
