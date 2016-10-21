FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir horizon-scanning
COPY requirements.txt requirements-dev.txt requirements-dep.txt /horizon-scanning/
WORKDIR horizon-scanning

# Install requirements
RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt

# Copy code
COPY . /horizon-scanning
COPY hstool/local_settings.py.docker hstool/local_settings.py

# Expose needed port
EXPOSE 8003

# Expose static volume
VOLUME /horizon-scanning/public/static

#Default command
CMD ["./docker-entrypoint.sh"]
