# Small python image
FROM python:3.9-slim-bullseye

WORKDIR /app

COPY sources/requirements.txt .

# We do not run pip update as we want to install a specific version of our
# requirements, which is already know by pip.
RUN pip install --no-cache-dir -r requirements.txt

# We copy the OCR_route.py file later to be able to modify it and rebuild
# without having to install requirements again.
COPY sources/OCR_routes.py .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "OCR_routes:app"]
