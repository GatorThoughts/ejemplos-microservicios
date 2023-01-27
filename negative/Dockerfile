#Tomar una imagen que tiene una instalación de Python
FROM python:3.10.9-slim-bullseye

#Environment variable que apunta al montaje de persistencia
ENV IMG_VOL /mnt/negatives/

WORKDIR /app

#Introducir ejecutable
COPY app.py /app/app.py

#Instalar dependencias detalladas en requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

#Levantar el servicio con gunicorn
ENTRYPOINT ["gunicorn", "app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000"]