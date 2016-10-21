FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir horizon_scanning
COPY requirements.txt requirements-dev.txt requirements-dep.txt /horizon_scanning/
WORKDIR horizon_scanning

# Install requirements
RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt

# Copy code
COPY . /horizon_scanning
COPY hstool/local_settings.py.docker hstool/local_settings.py

# Expose needed port
EXPOSE 8003

# Expose static volume
VOLUME /horizon_scanning/public/static

#Default command
CMD ["./docker-entrypoint.sh"]
