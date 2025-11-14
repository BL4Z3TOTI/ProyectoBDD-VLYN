from face_recognizer_lite import FaceRecognizerLite

img = "pruebaMessi.jpg"
db = "_pruebaFotos/"

fr = FaceRecognizerLite()

resultado = fr.predict(img, db)

if resultado:
    nombre = resultado["person"]
    distancia = resultado["distance"]
    umbral = 10.0  # ajustable

    prob = max(0, min(1, 1 - distancia / umbral))

    print("Persona probable:", nombre)
    print("Distancia:", distancia)
    print(f"Probabilidad de acierto: {prob*100:.2f}%")

else:
    print("No se encontró coincidencia")

