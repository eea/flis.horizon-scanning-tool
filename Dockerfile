# Pyhton image

FROM eeacms/python:2.7-slim

# Copy code into image
RUN mkdir horizon-scanning-tool
COPY . /horizon-scanning-tool
WORKDIR horizon-scanning-tool

# Install requirements
RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt
COPY hstool/local_settings.py.example hstool/local_settings.py
RUN ./manage.py collectstatic --noinput

# Expose needed port
EXPOSE 8003

# Expose static volume 
VOLUME /horizon-scanning-tool/static 

#Default command
CMD python ./manage.py runserver 0.0.0.0:8003

