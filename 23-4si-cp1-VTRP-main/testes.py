import cv2
import numpy as np
from pynput.keyboard import Key, Controller
import time

# Inicialização do teclado
keyboard = Controller()

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Valores dos filtros de cor
image_lower_hsv1 = np.array([140, 100, 40])
image_upper_hsv1 = np.array([175, 255, 255])
image_lower_hsv2 = np.array([50, 50, 50])
image_upper_hsv2 = np.array([80, 255, 255])

while True:
    # Leitura do frame da câmera
    ret, frame = cap.read()

    # Conversão do frame para o espaço de cor HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Aplicação dos filtros de cor
    filter1 = cv2.inRange(hsv_frame, image_lower_hsv1, image_upper_hsv1)
    filter2 = cv2.inRange(hsv_frame, image_lower_hsv2, image_upper_hsv2)
    filter = filter1 + filter2

    # Encontrar contornos na imagem filtrada
    contours, _ = cv2.findContours(filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar os dois maiores contornos
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    # Encontrar os centros dos contornos
    centers = []
    for contour in sorted_contours:
        moments = cv2.moments(contour)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
            centers.append((center_x, center_y))

    # Desenhar reta entre os centros dos contornos
    if len(centers) == 2:
        center1, center2 = centers
        cv2.line(frame, center1, center2, (0, 255, 0), 2)

        # Calcular o ângulo de inclinação da reta em relação ao plano horizontal
        angle = np.rad2deg(np.arctan2(center2[1] - center1[1], center2[0] - center1[0]))
        if angle < -169 or angle > 170:
            print("Pressionando w")
            keyboard.press('w')
            time.sleep(0.2)
            keyboard.release('w')
        elif -168 <= angle <= -145:
            print("Pressionando w+a")
            keyboard.press('w')
            keyboard.press('a')
            time.sleep(0.2)
            keyboard.release('w')
            keyboard.release('a')
        elif 145 <= angle <= 164:
            print("Pressionando w+d")
            keyboard.press('w')
            keyboard.press('d')
            time.sleep(0.2)
            keyboard.release('w')
            keyboard.release('d')     
        elif 20 <= angle <= 30:
            print("Pressionando w+a")
            keyboard.press('w')
            keyboard.press('a')
            time.sleep(0.2)
            keyboard.release('w')
            keyboard.release('a')

        # Escrever o ângulo na imagem
        cv2.putText(frame, f"Angulo: {angle:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Mostrar a imagem na tela
    cv2.imshow("Frame", frame)

     # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()