FROM python:3.9-bullseye

# Instala dependencias del sistema necesarias para OpenCV con Qt/X11
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 \
    libsm6 \
    libxfixes3 \
    libqt5gui5 \
    libusb-1.0-0 \
    libasound2 \
    libappindicator3-1 \
    libqt5core5a \
    libqt5widgets5 \
    qtbase5-dev \
    ffmpeg \
    v4l2loopback-dkms \
    v4l2loopback-utils \
    kmod \
    && rm -rf /var/lib/apt/lists/*


# Instala las librerías de Python con binarios precompilados
RUN pip install --no-cache-dir \
    mysql-connector-python \
    opencv-python \
    mediapipe \
    deepface[opencv] \
    numpy


# Directorio de trabajo
WORKDIR /app

# Copia tu código (ajustá según tu estructura)
COPY . .


# Script para iniciar IP Webcam stream
COPY start_webcam.sh /start_webcam.sh
RUN chmod +x /start_webcam.sh

# Mantiene el contenedor corriendo (para debug o pruebas)
CMD ["tail", "-f", "/dev/null"]


