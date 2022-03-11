import os


from flask import Flask, request, jsonify


from celery import Celery
from celery.result import AsyncResult

# Celery configuration
CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]  # 'amqp://???:???@???:5672/'
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]  # 'rpc://'


# Initialize Celery
celeryapp = Celery(broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celeryapp.config_from_object('celeryconfig')


app = Flask(__name__)

@app.route('/check', methods=['get'])
def check():
    return "Hello"

@app.route('/ocr', methods=['POST'])
def ocr():
    """Compute transcriptions of given document image.

        Layout extraction will be performed to detect lines.

        Response content is JSON payload with responses in the following format:  
        ```
        { 
            "software": "pero ocr ...",
            "content": "text"
        }
        ```

        Example (Python):
        ```
        response = requests.post(
            url=f"{server_uri}/ocr/",
            data=image_data)
        print(response.json()["content"])
        ```

        Example (curl):
        ```
        curl -X POST \
        --url http://localhost:8000/ocr \
        --header "Content-type: image/jpg" \
        -T text.jpg
        ```
    """

    image_data = request.data
    # We expect image/jpg Content type
    if image_data is None:
        # FIXME (Joseph) unclear json schema for results (should always contain the same fields, plus extra opt fields)
        return jsonify({"error": "Request contains no image data."}), 500
    r = celeryapp.send_task('worker.run_ocr', args=(image_data,), serializer="pickle")
    return jsonify({ "submitted" : r.id })


@app.route('/results/<task_id>', methods=['GET'])
def trigger_task_res(task_id):
    result = AsyncResult(task_id, app=celeryapp)
    if result.ready():
        return jsonify({ "content" : result.get() })
    if result.failed():
        return jsonify({ "state" : result.state, "error": result.traceback })
    return jsonify({ "state" : result.state })

# TODO (Joseph) add forget route

# TODO (Joseph) handle auth and task per-user task isolation
