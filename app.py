from flask import Flask
import models

app = Flask(__name__)
app.config.from_pyfile('.env')
models.init_db(app)


@app.route("/")
def index():
    return "Hello from flask"


if __name__ == "__main__":
    app.run(debug=True)
