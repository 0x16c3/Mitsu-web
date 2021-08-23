import os

from entry import app
from flask import send_from_directory
from api.utils import serve_image, generate_error

import api.filter
import api.character


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(404)
def page_not_found(e):
    return serve_image(generate_error(title="Unknown endpoint.", error=str(e)))


@app.route("/")
def main():
    return ""


if __name__ == "__main__":
    app.run(debug=False)
