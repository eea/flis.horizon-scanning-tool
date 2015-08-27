FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir horizon-scanning-tool
COPY requirements.txt requirements-dev.txt requirements-dep.txt /horizon-scanning-tool/
WORKDIR horizon-scanning-tool

# Install requirements
RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt

# Copy code
COPY . /horizon-scanning-tool
RUN ./manage.py collectstatic --noinput
COPY hstool/local_settings.py.docker hstool/local_settings.py

# Expose needed port
EXPOSE 8003

# Expose static volume 
VOLUME /horizon-scanning-tool/public/static

#Default command
CMD gunicorn hstool.wsgi:application --bind 0.0.0.0:8003

