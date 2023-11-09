# Dockerfile, Image, Container
FROM python:3.10

#ADD *.py .
#ADD db_credentials.json .

#RUN pip install --no-cache-dir --upgrade scikit-learn
#RUN pip install --no-cache-dir --upgrade mysql-connector-python

#CMD ["python", "./main.py"]

WORKDIR /custom-settings
COPY ./custom-settings /custom-settings

WORKDIR /assets
COPY ./assets /assets

WORKDIR /build
COPY ./requirements.txt /build/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /build/requirements.txt

COPY ./src /build


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
