

import cv2
import pandas as pd
from deepface import DeepFace

import os
import time


class ControladorBiometrico():

    def _init_(self):
        self.filename = "imgPrueba.jpg"
        self.color = (0,255,0)
    

    def registrarParametrosBiometricos(self, rol,username):

        output_dir = f"_dbRostros/{rol}/{username}"
        os.makedirs(output_dir, exist_ok=True)

        cap = cv2.VideoCapture(0)

        # Configura resolución baja para mejor rendimiento
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 20)

        cantImgs = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR CON LA CAMARA!!!")
                break
    
            cv2.putText(frame, "Capture imagenes con la tecla espacio, tecla escape sale", 
            (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0,9, self.color, 2)


            key = cv2.waitKey(1) & 0xFF
    
            if key == 32:
                cantImgs = cantImgs +1
                filename = f"{output_dir}"/img{cantImgs}.jpg"
                cv2.imwrite(filename, frame)
                print(" FOTO GUARDADA", filename)
                time.sleep(0.5)
            

            if key == 27 and cantImgs>5:
                break


        cap.release()
        cv2.destroyAllWindows()
        print(" Captura finalizada correctamente.")

    def reconocerRostro(self, tipoUsuario):

        cap = cv2.VideoCapture(0)
        username = ""
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR CON LA CAMARA")
                break
            
            cv2.putText(frame, "Espacio = capturar | ESC = salir", (10,20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.color, 2)

            cv2.imshow("Camara", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == 32:
                cv2.imwrite(self.filename, frame)
                username = self.verRostroValido(tipoUsuario)

                # BORRAR IMAGEN TEMPORAL
                if os.path.exists(self.filename):
                    os.remove(self.filename)
                break
                
            if key == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return username

    def verRostroValido(self, tipoUsuario):

        print(tipoUsuario)

            # Validar tipo
        if tipoUsuario not in ["estudiantes", "profes"]:
            print("Tipo inválido:", tipoUsuario)
            return ""

        # Base de datos de rostros
        db = f"_dbRostros/{tipoUsuario}"

        username = ""
        # Buscar coincidencias
        resultados = DeepFace.find(img_path=self.filename, db_path=db, model_name="ArcFace",  
        enforce_detection=False )

         # Validar resultado
        if resultados is None or len(resultados) == 0:
            print("Sin coincidencias detectadas.")
            return ""

        df = resultados[0]
        if df.shape[0] == 0:
            print("No hay matches en el DataFrame.")
            return ""
 

        if df.shape[0] > 0:
            match = df.iloc[0].to_dict()  # mejor coincidencia
            # Extraemos el nombre de la carpeta
            username = match["identity"].replace("\\","/").split("/")[-2]

            # Distancia del embedding
            distancia = match["distance"]
    
            # Umbral recomendado para ArcFace
            umbral = 0.40

            print("Persona probable:", nombre)
            print("Distancia:", distancia)
        
        return username

    