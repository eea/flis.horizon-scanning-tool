# Pyhton image

FROM python:2.7-slim

# System requirements

RUN apt-get -y update && apt-get -y install \
    gcc \
    python-setuptools \
    python-dev \
    python-mysqldb \
    libxml2-dev \
    libxslt1-dev \
    lib32z1-dev \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev

# Copy code into image

RUN mkdir horizon-scanning-tool
COPY . /horizon-scanning-tool
WORKDIR horizon-scanning-tool

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt
COPY hstool/local_settings.py.example hstool/local_settings.py

# Expose needed port

EXPOSE ${APP_PORT}

#Default command

CMD python ./manage.py runserver 0.0.0.0:8000
