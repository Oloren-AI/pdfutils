# Base Image
FROM python:3.10-slim-bullseye

# Installing necessary packages
RUN pip install oloren
RUN pip install pandas numpy
RUN pip install PyPDF2

RUN pip install -U pypdfium2
RUN pip install Pillow
RUN pip install "python-socketio[client]"

# Copying application code to the Docker image
COPY app.py /app.py

# Default command for the container
CMD ["python", "app.py"]