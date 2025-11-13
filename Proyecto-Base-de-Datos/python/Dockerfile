FROM python:3.9-slim

# Instala dependencias del sistema necesarias para OpenCV con Qt/X11
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    libqt5gui5 \
    libqt5core5a \
    libqt5widgets5 \
    qtbase5-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


# Instala las librerías de Python con binarios precompilados
RUN pip install --no-cache-dir \
    mysql-connector-python \
    opencv-python \
    mediapipe

# Directorio de trabajo
WORKDIR /app

# Copia tu código (ajustá según tu estructura)
COPY . .

# Mantiene el contenedor corriendo (para debug o pruebas)
CMD ["tail", "-f", "/dev/null"]


