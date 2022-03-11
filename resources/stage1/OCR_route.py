from io import BytesIO
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import cv2


app = Flask(__name__)


@app.route("/imgshape", methods=["POST"])
def imgshape():
    image_data = request.data
    # We expect image/jpg Content type
    if image_data is None:
        return jsonify({"error": "Request contains no image data."}), 500

    width = height = depth = None

    with tempfile.TemporaryDirectory() as tmpdirname:
        # TODO write image to disk (unless you find a better way)
        # ...
        try:
            pass
            # TODO use opencv (headless) or some better choice to read the image and get its shape
            # ...
        except Exception as err:
            return jsonify({"error": f"Unknown error: {err}"}), 500

    return jsonify({"content": {"width": width, "height": height, "depth": depth}}), 200


if __name__ == "__main__":
    # Simply running this file will start a Flask server in development mode.
    app.run(host="0.0.0.0", debug=True)
