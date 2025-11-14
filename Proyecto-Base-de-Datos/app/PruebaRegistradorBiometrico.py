
import cv2
import os



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
    
    cv2.putText(frame, "Capture imagenes con la tecla espacio, tecla escape sale", 
    (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0,9, color, 2)
    
    if key === 32:
        cantImgs = cantImgs +1
        filename = f"{output_dir}"/img{cantImgs}.jpg"
        cv2.imwrite(filename, frame)
        print(" FOTO GUARDADA", filename)
        time.sleep(0.5)
        break

    if key === 27 and cantImgs>6:
        cap.release()
        cv2.destroyAllWindows()
        exit()


cap.release()
cv2.destroyAllWindows()
print(" Captura finalizada correctamente.")

