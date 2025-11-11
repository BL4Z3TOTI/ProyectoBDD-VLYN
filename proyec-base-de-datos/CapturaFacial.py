import cv2
import face_recognition
import numpy as np
import time

def generar_encoding_facial(frames_necesarios=30):
    """
    Captura la cara del usuario durante varios frames, genera el encoding
    facial promedio y lo devuelve como un string para guardar en la BD.
    """
    cap = cv2.VideoCapture(0) # Inicia la cámara
    if not cap.isOpened():
        print("ERROR: No se pudo acceder a la cámara.")
        return None

    encodings_capturados = []
    frames_capturados = 0
    
    print("--- INICIO DE CAPTURA FACIAL ---")
    print(f"Por favor, mantén tu cara visible en el centro de la cámara (necesario: {frames_necesarios} frames).")

    while frames_capturados < frames_necesarios:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir BGR a RGB (requerido por face_recognition)
        rgb_frame = frame[:, :, ::-1]

        # Encontrar caras en el frame
        face_locations = face_recognition.face_locations(rgb_frame)
        
        # Procesar solo si se detecta una cara
        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            encodings_capturados.append(face_encoding)
            frames_capturados += 1
            
            # Dibujar un rectángulo verde alrededor de la cara
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"Capturando... {frames_capturados}/{frames_necesarios}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        else:
            cv2.putText(frame, "No se detecta una cara o hay varias.", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Mostrar el frame
        cv2.imshow('Registro Facial', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Limpiar recursos
    cap.release()
    cv2.destroyAllWindows()
    
    if len(encodings_capturados) < frames_necesarios:
        print(f"ERROR: Se capturaron solo {len(encodings_capturados)} de {frames_necesarios} frames. Registro cancelado.")
        return None

    # Calcular el promedio de todos los encodings capturados (más robusto)
    promedio_encoding = np.mean(encodings_capturados, axis=0)

    # Convertir el array numpy a un string separado por comas para guardar en la DB
    encoding_str = ",".join(map(str, promedio_encoding))
    print("Captura facial completada con éxito.")
    return encoding_str

def iniciar_login_facial():
    """Captura la cara del usuario en tiempo real y devuelve el encoding promedio para la busqueda."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: No se pudo acceder a la cámara.")
        return None

    frame_count = 0
    max_frames = 10 
    encodings_capturados = []
    
    print("--- INICIO DE SESIÓN FACIAL ---")
    print("Por favor, mira a la cámara para iniciar sesión...")

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            encodings_capturados.append(face_encoding)
            
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "DETECTADO", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            frame_count += 1
        else:
            cv2.putText(frame, "Buscando cara...", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Login Facial', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    if len(encodings_capturados) == 0:
        return None
    
    # Usar el promedio de los frames capturados
    promedio_encoding = np.mean(encodings_capturados, axis=0)
    return promedio_encoding