
import cv2
import os
import time


output_dir = f"_pruebaFotos/carlos"
os.makedirs(output_dir, exist_ok=True)


color = (0,255,0)

cap = cv2.VideoCapture(0)
cantImgs = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR CON LA CAMARA!!!")
        break
    
    # Texto en pantalla
    cv2.putText(frame, 
        "Captura con ESPACIO - Salir con ESC", 
        (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv2.imshow("Camara", frame)

    key = cv2.waitKey(1) & 0xFF
    
    if key == 32:
        cantImgs = cantImgs +1
        filename = f"{output_dir}/img{cantImgs}.jpg"
        cv2.imwrite(filename, frame)
        print(" FOTO GUARDADA", filename)
        time.sleep(0.5)

    if key == 27 and cantImgs>5:
        break


cap.release()
cv2.destroyAllWindows()
print(" Captura finalizada correctamente.")

