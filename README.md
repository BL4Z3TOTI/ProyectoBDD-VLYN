# ProyectoBDD-VLYN 

Para probarlo, entrar a la carpeta Proyecto-Base-De-Datos: 

   Modificar el ./Proyecto-Base-De-Datos/docker-compose.yml y el ./Proyecto-Base-De-Datos/python/Dockerfile 
 con la ip correspondiente que te muestra IPWEBCAM

   La primera vez, ejecutar el comando 
 
      docker compose up --build -d

   (tarda un rato)
   el comando --build es para buildear desde cero la imagen, siguientes corridas no debería estar
   el comando -d es para que pueda salir de la terminal y no quedarse corriendo (modo detached)


   # 1. En HOST: Carga el módulo y verifica
      
    sudo modprobe v4l2loopback exclusive_caps=1 video_nr=0
    v4l2-ctl --list-devices

   # 2. En HOST: Inicia el stream (en una terminal separada)
   
    ffmpeg -i http://IP_QUE_MARCA_IPWEBCAM:8080/video -vf "scale=960:540,format=yuv420p" -f v4l2 /dev/video0

   # 3. En HOST: Prueba que funciona
   
    ffplay /dev/video0

   # 4. En HOST: Da permisos X11 si usas Docker
  
     xhost +local:docker
   

   Luego de las configuraciones del HOST, entrar  al contenedor de python (donde está el código)

        docker exec -it python_client bash

   ahi entrarán en el bash del contenedor, pudiendo correr cualquier script de este


