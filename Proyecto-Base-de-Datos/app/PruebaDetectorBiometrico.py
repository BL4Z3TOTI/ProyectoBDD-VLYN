import pandas as pd
from deepface import DeepFace

# Imagen a identificar
img = "messiPrueba.png"

# Base de datos de rostros
db = "_pruebaFotos/"

# Buscar coincidencias
resultados = DeepFace.find(img_path=img, db_path=db, model_name="ArcFace",     enforce_detection=False )

# result es una lista → tomamos el primer DataFrame
df = resultados[0]

if df.shape[0] > 0:
    match = df.iloc[0].to_dict()  # mejor coincidencia
    # Extraemos el nombre de la carpeta
    nombre = match["identity"].replace("\\","/").split("/")[-2]

        # Distancia del embedding
    distancia = match["distance"]
    
    # Umbral recomendado para ArcFace
    umbral = 0.40

    print("Persona probable:", nombre)
    print("Distancia:", distancia)
        # Probabilidad estimada (acotada entre 0 y 1)
    prob = max(0, min(1, 1 - distancia / umbral))

    print(f"Probabilidad de acierto: {prob*100:.2f}%")
else:
    print("No se encontró coincidencia")