import numpy as np
import os
import time

from PIL import Image, UnidentifiedImageError
from flask import Flask, request, jsonify
from io import BytesIO
from pero_ocr_driver import PERO_driver

app = Flask(__name__)


@app.route("/imgshape", methods=["POST"])
def imgshape():
    image_data = request.data
    # We expect image/jpg Content type
    if image_data is None:
        return jsonify({"error": "Request contains no image data."}), 500

    width = height = depth = None

    # write image to disk (unless you find a better way)
    try:
        # use opencv (headless) or some better choice to read the image and get its shape
        image = Image.open(BytesIO(image_data))
        width, height = image.size
        depth = len(image.getbands())
    except UnidentifiedImageError:
        return jsonify({"error": "Cannot open image."}), 422
    except Exception as err:
        return jsonify({"error": f"Unknown error: {err}"}), 500

    return jsonify({"content": {"width": width, "height": height, "depth": depth}}), 200


@app.route("/ocr", methods=["POST"])
def ocr():
    # Init the OCR engine if needed
    start_time = time.time()
    ocr_engine = PERO_driver(os.environ["PERO_CONFIG_DIR"])
    elapsed_time = int((time.time() - start_time) * 1000)
    print("init 'pero ocr engine' performed in %.1f ms.", elapsed_time)

    # TODO reuse previous code from the /imgshape/ route to read the image content
    # `img` should be a valid numpy array representing an image in what follows
    image_data = request.data
    # We expect image/jpg Content type
    if image_data is None:
        return jsonify({"error": "Request contains no image data."}), 500

    # Retrieve the image from bytes
    try:
        image = Image.open(BytesIO(image_data))
    except UnidentifiedImageError:
        return jsonify({"error": "Cannot open image."}), 422
    except Exception as err:
        return jsonify({"error": f"Unknown error: {err}"}), 500

    # Convert the image to a numpy array
    img = np.array(image)

    # Perform the actual computation
    ocr_results = ocr_engine.detect_and_recognize(img)
    ocr_results = "\n".join([textline.transcription for textline in ocr_results])
    print(ocr_results)

    # Return result as json payload
    return jsonify({"content": ocr_results}), 200


@app.route("/check")
def check():
    return "Hello\n"


if __name__ == "__main__":
    # Simply running this file will start a Flask server in development mode.
    app.run(host="0.0.0.0", debug=True)
