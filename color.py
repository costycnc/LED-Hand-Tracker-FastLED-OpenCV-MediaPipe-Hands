import cv2
import mediapipe as mp
import serial
import time

# ---------- Config ----------
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Cerchi RGB in alto (X, Y, Raggio, Colore BGR)
circles = [
    {"center": (150, 100), "radius": 50, "color": (0,0,255), "name": "Rosso"},   # BGR
    {"center": (320, 100), "radius": 50, "color": (0,255,0), "name": "Verde"},
    {"center": (490, 100), "radius": 50, "color": (255,0,0), "name": "Blu"}
]

# Serial setup: modifica porta COM per il tuo PC
ser = serial.Serial("COM3", 115200, timeout=1)
time.sleep(2)  # attende apertura seriale

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.65, min_tracking_confidence=0.65)

cap = cv2.VideoCapture(0)
prev_color = None  # per evitare invii ripetuti

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Disegna i cerchi RGB
    for c in circles:
        cv2.circle(frame, c["center"], c["radius"], c["color"], -1)

    slider_value = None

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        tip_index = hand.landmark[8]

        # coordinate punta indice in pixel
        x_tip = int(tip_index.x * WINDOW_WIDTH)
        y_tip = int(tip_index.y * WINDOW_HEIGHT)

        # Disegna cerchio sulla punta del dito
        cv2.circle(frame, (x_tip, y_tip), 10, (0,255,255), -1)

        # Controlla se tocca qualche cerchio
        color_touched = None
        for c in circles:
            dx = x_tip - c["center"][0]
            dy = y_tip - c["center"][1]
            dist = (dx**2 + dy**2)**0.5
            if dist <= c["radius"]:
                color_touched = c["name"]
                break

        if color_touched is not None and color_touched != prev_color:
            print(f"Colore selezionato: {color_touched}")
            # invia colore via seriale
            ser.write(f"{color_touched}\n".encode())
            prev_color = color_touched
        elif color_touched is None:
            prev_color = None

    cv2.imshow("Selezione Colore WS2812", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
ser.close()
