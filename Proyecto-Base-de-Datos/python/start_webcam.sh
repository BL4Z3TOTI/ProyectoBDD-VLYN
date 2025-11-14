#!/bin/bash
# Script para iniciar IP Webcam como dispositivo de video

IP_WEBCAM_URL=${IP_WEBCAM_URL:-"http://192.168.0.36:8080/video"}
VIDEO_DEVICE=${VIDEO_DEVICE:-"/dev/video0"}

echo "Conectando a IP Webcam en: $IP_WEBCAM_URL"
echo "Creando dispositivo de video en: $VIDEO_DEVICE"

# Inicia ffmpeg para crear el dispositivo virtual
ffmpeg -i "$IP_WEBCAM_URL" \
    -vf "scale=640:480,format=yuv420p" \
    -f v4l2 "$VIDEO_DEVICE"


