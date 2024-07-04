# Usa una imagen base oficial de Python
FROM python:3.9

# Establece el directorio de trabajo en la imagen de Docker
WORKDIR /app

# Copia el archivo de requisitos en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación en el directorio de trabajo
COPY . .

# Expone el puerto en el que la aplicación va a correr
EXPOSE 5000

# Define el comando por defecto que se ejecutará cuando el contenedor inicie
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
