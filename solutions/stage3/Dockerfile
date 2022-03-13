# Small python image
FROM python:3.9-slim-bullseye

# Download and install Pero OCR
RUN pip install --no-cache-dir https://github.com/jchazalon/pero-ocr/archive/refs/heads/master.zip

WORKDIR /app

# Download given tar
ADD https://www.lrde.epita.fr/~jchazalo/SHARE/pero_eu_cz_print_newspapers_2020-10-09.tar.gz ./

# Untar and clean it
RUN tar -xvf ./pero_eu_cz_print_newspapers_2020-10-09.tar.gz && rm ./pero_eu_cz_print_newspapers_2020-10-09.tar.gz

ENV PERO_CONFIG_DIR=/app/pero_eu_cz_print_newspapers_2020-10-07

COPY sources/requirements.txt .

# We do not run pip update as we want to install a specific version of our
# requirements, which is already know by pip.
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ADD https://download.pytorch.org/models/vgg16-397923af.pth /root/.cache/torch/hub/checkpoints/vgg16-397923af.pth

# We copy the OCR_route.py file later to be able to modify it and rebuild
# without having to install requirements again.
COPY sources/*.py ./

CMD ["gunicorn", "-b", "0.0.0.0:8000", "OCR_routes:app"]
