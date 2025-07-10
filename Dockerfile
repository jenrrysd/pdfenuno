FROM python:3.11-slim-bookworm

# Configura el entorno
WORKDIR /app
#ENV FLASK_APP=app.py
#ENV FLASK_ENV=production

RUN apt-get update -y && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*
# Copia los archivos necesarios
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Crea carpetas para los PDFs temporales
RUN mkdir -p /app/static/uploads /app/static/outputs

# Expone el puerto donde Flask corre (5000 por defecto)
EXPOSE 2020

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:2020", "app:app"]