import cv2
import numpy as np

#importes para emular precionamento de teclas
from pynput.keyboard import Key, Controller
import pynput
import time
import random

keys = [
    #Key.up,                                 # UP
    #Key.down,                               # DOWN
    #Key.left,                               # LEFT
    #Key.right,                              # RIGHT
    pynput.keyboard.KeyCode.from_char('w'),  # A
    pynput.keyboard.KeyCode.from_char('d'),  # B
    pynput.keyboard.KeyCode.from_char('a'),  # X
    #Key.enter,                              # START
    #Key.shift_r,                            # SELECT
]

# Inicializa o objeto do teclado
keyboard = Controller()

# Define os filtros de cor HSV
image_lower_hsv1 = np.array([140, 100, 40])
image_upper_hsv1 = np.array([175, 255, 255])
image_lower_hsv2 = np.array([50, 50, 50])
image_upper_hsv2 = np.array([80, 255, 255])

# Captura o vídeo da câmera
cap = cv2.VideoCapture(0)

while True:
    # Lê um frame do vídeo
    ret, frame = cap.read()
    
    # Converte o frame para o espaço de cores HSV
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Aplica os filtros de cor HSV
    mask1 = cv2.inRange(frame_hsv, image_lower_hsv1, image_upper_hsv1)
    mask2 = cv2.inRange(frame_hsv, image_lower_hsv2, image_upper_hsv2)
    
    # Combina as máscaras usando um operador OR
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Encontra os contornos na imagem filtrada
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) >= 2:
        # Encontra os dois maiores contornos
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        
        # Encontra os centros dos dois contornos
        centers = []
        for contour in contours:
            moments = cv2.moments(contour)
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
            centers.append((center_x, center_y))
        
        # Desenha uma linha entre os dois centros
        cv2.line(frame, centers[0], centers[1], (0, 0, 255), 2)
        
        # Calcula o ângulo de inclinação da reta em relação ao plano horizontal
        delta_x = centers[1][0] - centers[0][0]
        delta_y = centers[1][1] - centers[0][1]
        angle = np.degrees(np.arctan2(delta_y, delta_x))
        
        # Exibe o ângulo na tela
        cv2.putText(frame, f"Angle: {angle:.2f} degrees", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Emula o pressionamento da tecla 'space' se o ângulo for menor que 5 graus
        if abs(angle) < 5:
            keyboard.press(' ')
            keyboard.release(' ')
    
    # Exibe o frame na janela
    cv2.imshow("Frame", frame)
    
    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()