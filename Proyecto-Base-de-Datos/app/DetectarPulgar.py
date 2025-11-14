
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

def detectar_pulgar_arriba():
    cap = cv2.VideoCapture(0)
    # Configura resolución baja para mejor rendimiento
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 20)

    PUNTAS_DEDOS = [8, 12, 16, 20]
    SEGUNDOS_NUDILLOS = [7, 11, 15, 19]

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    
                    punta_pulgar_y = hand_landmarks.landmark[4].y
                    base_mano_y = hand_landmarks.landmark[0].y
                    
                    pulgar_levantado = punta_pulgar_y < base_mano_y
                    
                    dedos_doblados = True
                    for punta_idx, nudillo_idx in zip(PUNTAS_DEDOS, SEGUNDOS_NUDILLOS):
                        punta_y = hand_landmarks.landmark[punta_idx].y
                        nudillo_y = hand_landmarks.landmark[nudillo_idx].y
                        
                        if punta_y < nudillo_y - 0.05:
                            dedos_doblados = False
                            break
                            
                    if pulgar_levantado and dedos_doblados:
                        cap.release()
                        cv2.destroyAllWindows()
                        return True
                        
            cv2.imshow('Camara - Gesto de Voto', image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()
    return False

if __name__ == "__main__":
    if detectar_pulgar_arriba():
        print("✅ Gesto de Pulgar Arriba detectado con éxito.")
    else:
        print("❌ Gesto no detectado.")
