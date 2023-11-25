# Dockerfile, Image, Container
FROM python:3.10

#ADD *.py .
#ADD db_credentials.json .

#RUN pip install --no-cache-dir --upgrade scikit-learn
#RUN pip install --no-cache-dir --upgrade mysql-connector-python

#CMD ["python", "./main.py"]

WORKDIR /cache
WORKDIR /logs
WORKDIR /custom-configuration
WORKDIR /assets

WORKDIR /build
COPY ./requirements.txt /build/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /build/requirements.txt
#at the moment install the specific branch in which the calendar is already implemented
RUN pip install --no-cache-dir --upgrade git+https://github.com/bensteUEM/ChurchToolsAPI.git@dev_benste
#RUN pip install --no-cache-dir --upgrade git+https://github.com/bensteUEM/ChurchToolsAPI.git

COPY ./static /static
COPY ./custom-configuration /custom-configuration
COPY ./secret /secret
COPY ./src /build


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
