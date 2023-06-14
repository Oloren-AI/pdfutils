# Base Image
FROM python:3.10-slim-bullseye

# Installing necessary packages
RUN pip install oloren
RUN pip install pandas numpy scikit-learn matplotlib seaborn

# Copying application code to the Docker image
COPY app.py /app.py

# Default command for the container
CMD ["python", "app.py"]