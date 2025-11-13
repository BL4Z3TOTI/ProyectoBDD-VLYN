# ProyectoBDD-VLYN



Para probarlo:
   primera vez
 
      docker compose up --build -d

   el comando --build es para buildear desde cero la imagen, siguientes corridas no debería estar
   el comando -d es para que pueda salir de la terminal y no quedarse corriendo (modo detached)


   Si van a probar la cámara poner este comando:
    
       xhost +local:root

   para entrar al contenedor de python (donde está el código)

        docker exec -it python_client bash

   ahi entrarán en el bash del contenedor, pudiendo correr cualquier script de este


