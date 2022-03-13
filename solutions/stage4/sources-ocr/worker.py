from celery import Celery
from io import BytesIO
from pero_ocr_driver import PERO_driver
from PIL import Image, UnidentifiedImageError
import numpy as np
import os

# Celery configuration
CELERY_BROKER_URL = os.environ[
    "CELERY_BROKER_URL"
]  # 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]  # 'rpc://'


# PERO configuration
PERO_CONFIG_DIR = os.environ["PERO_CONFIG_DIR"]

# Initialize Celery
celery = Celery(
    "worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND
)  # 'ocr_worker',
celery.config_from_object("celeryconfig")

# Define our OCR task
@celery.task()
def run_ocr(image_data):
    # We expect image/jpg Content type
    if image_data is None:
        return {"error": "Request contains no image data."}

    try:
        image = Image.open(BytesIO(image_data))
        img = np.array(image)
    except UnidentifiedImageError:
        return {"error": "Cannot open image."}, 422
    except Exception as err:
        return {"error": f"Unknown error: {err}"}

    ocr_engine = PERO_driver(PERO_CONFIG_DIR)
    ocr_results = ocr_engine.detect_and_recognize(img)
    ocr_results = "\n".join([textline.transcription for textline in ocr_results])
    return {"content": ocr_results}
