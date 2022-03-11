from io import BytesIO
import os
from pathlib import Path
import tempfile

from pero_ocr_driver import PERO_driver

from celery import Celery
import cv2

# Celery configuration
CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]  # 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]  # 'rpc://'


# PERO configuration
PERO_CONFIG_DIR = os.environ["PERO_CONFIG_DIR"]

# Initialize Celery
celery = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND) # 'ocr_worker', 
celery.config_from_object('celeryconfig')

# Define our OCR task
@celery.task()
def run_ocr(image_data):
    # We expect image/jpg Content type
    if image_data is None:
        return {"error": "Request contains no image data."}

    with tempfile.TemporaryDirectory() as tmpdirname:
        imagepath = Path(tmpdirname) / "input.jpg"
        with open(imagepath, 'wb') as out_file:
            out_file.write(BytesIO(image_data).getbuffer())

        try:
            img = cv2.imread(str(imagepath))
            if img is None:
                return {"error": "Cannot open image."}
        except Exception as err:
            return {"error": f"Unknown error: {err}"}

    ocr_engine = PERO_driver(PERO_CONFIG_DIR)
    ocr_results = ocr_engine.detect_and_recognize(img)
    ocr_results = "\n".join([textline.transcription for textline in ocr_results])
    return {"content": ocr_results}
