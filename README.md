# ProyectoBDD-VLYN

Este proyecto utiliza **IP Webcam**, **FFmpeg**, **v4l2loopback** y un contenedor Docker con Python para procesar un stream de video como si fuera una cámara virtual.

A continuación se describen los pasos para configurar el entorno tanto en el **host** como en el **contenedor Docker**.

---

## 📁 Preparación del proyecto

1. Ingresar a la carpeta principal:

```
Proyecto-Base-De-Datos/
```

2. Modificar los siguientes archivos para colocar la **IP que muestra IP Webcam**:

   * `./Proyecto-Base-De-Datos/docker-compose.yml`
   * `./Proyecto-Base-De-Datos/python/Dockerfile`

   Reemplazar donde corresponda `IP_QUE_MARCA_IPWEBCAM`.

---

## 🚀 Ejecución inicial del entorno

La primera vez ejecutar:

```
docker compose up --build -d
```

* `--build` reconstruye las imágenes desde cero (solo necesario la primera vez o si cambian los Dockerfiles).
* `-d` ejecuta los servicios en modo *detached*, dejándote liberar la terminal.

---

## 🖥️ Configuración en el HOST

### 1️⃣ Cargar módulo v4l2loopback y verificar

```
sudo modprobe v4l2loopback exclusive_caps=1 video_nr=0
v4l2-ctl --list-devices
```

### 2️⃣ Iniciar el stream desde IP Webcam (en una terminal separada)

```
ffmpeg -i http://IP_QUE_MARCA_IPWEBCAM:8080/video -vf "scale=960:540,format=yuv420p" -f v4l2 /dev/video0
```

### 3️⃣ Probar que la cámara virtual funciona

```
ffplay /dev/video0
```

### 4️⃣ Permitir acceso gráfico a Docker (si corres aplicaciones GUI)

```
xhost +local:docker
```

---

## 🐍 Ingreso al contenedor Python

Cuando el host ya está configurado y el contenedor levantado:

```
docker exec -it python_client bash
```

Esto abre una terminal dentro del contenedor, desde donde podrás ejecutar cualquier script del proyecto.

---

## ✅ Todo listo

Con estos pasos completados, el contenedor Python podrá acceder al stream proveniente de IP Webcam como si fuera una cámara física accesible en `/dev/video0`.

