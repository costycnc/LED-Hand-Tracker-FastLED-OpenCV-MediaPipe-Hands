import cv2
import mediapipe as mp
import serial
import time
import math

# ---------- Config ----------
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Cerchi RGB più piccoli, posizionati verso la base
circles = [
    {"center": (150, 400), "radius": 30, "color": (0,0,255), "name": "RED"},
    {"center": (320, 400), "radius": 30, "color": (0,255,0), "name": "GREEN"},
    {"center": (490, 400), "radius": 30, "color": (255,0,0), "name": "BLUE"}
]

# Slider (da 0 a 10)
slider_start = (100, 300)   # punto iniziale (x,y)
slider_end   = (540, 300)   # punto finale (x,y)
slider_value = 0            # valore iniziale
slider_max   = 10

# Serial setup: modifica porta COM per il tuo PC
ser = serial.Serial("COM5", 115200, timeout=1)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.65, min_tracking_confidence=0.65)

cap = cv2.VideoCapture(0)
prev_trigger = None
DIST_THRESHOLD = 40
glow_state = 0
prev_slider_value = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
    frame = cv2.flip(frame, 1)  # specchio
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    trigger_color = None

    # Effetto bagliore
    glow_state = (glow_state + 1) % 20
    glow_radius = 5 + (glow_state if glow_state < 10 else 20 - glow_state)

    # Disegna i cerchi RGB
    for c in circles:
        cv2.circle(frame, c["center"], c["radius"], c["color"], -1)

    # Disegna slider
    cv2.line(frame, slider_start, slider_end, (200,200,200), 4)
    slider_pos_x = int(slider_start[0] + (slider_value/slider_max) * (slider_end[0] - slider_start[0]))
    cv2.circle(frame, (slider_pos_x, slider_start[1]), 12, (0,255,255), -1)
    cv2.putText(frame, f"Value: {slider_value}", (slider_end[0]+20, slider_start[1]+5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        # Coordinate pollice e indice
        thumb_tip = hand.landmark[4]
        index_tip = hand.landmark[8]

        x_thumb = int(thumb_tip.x * WINDOW_WIDTH)
        y_thumb = int(thumb_tip.y * WINDOW_HEIGHT)
        x_index = int(index_tip.x * WINDOW_WIDTH)
        y_index = int(index_tip.y * WINDOW_HEIGHT)

        dist = math.hypot(x_thumb - x_index, y_thumb - y_index)

        if dist < DIST_THRESHOLD:
            # Punto medio tra le dita
            mid_x = (x_thumb + x_index) // 2
            mid_y = (y_thumb + y_index) // 2

            # Controllo cerchi colori
            for c in circles:
                dx = mid_x - c["center"][0]
                dy = mid_y - c["center"][1]
                circle_dist = math.hypot(dx, dy)
                if circle_dist <= c["radius"]:
                    trigger_color = c["name"]
                    cv2.circle(frame, c["center"], c["radius"] + glow_radius, (0,255,255), 3)
                    break

            # Controllo slider (vicino alla linea)
            dist_line = abs(mid_y - slider_start[1])
            if dist_line < 25 and slider_start[0] <= mid_x <= slider_end[0]:
                # Mappa posizione X a valore 0-10
                slider_value = int(((mid_x - slider_start[0]) / (slider_end[0] - slider_start[0])) * slider_max)

    # Invio seriale per colori
    if trigger_color and trigger_color != prev_trigger:
        print(f"Colore selezionato: {trigger_color}")
        ser.write(f"{trigger_color}\n".encode())
        prev_trigger = trigger_color
    elif trigger_color is None:
        prev_trigger = None

    # Invio seriale per slider
    if slider_value != prev_slider_value:
        print(f"Slider: {slider_value}")
        ser.write(f"SLIDER:{slider_value}\n".encode())
        prev_slider_value = slider_value

    cv2.imshow("Selezione Colore + Slider con Dita", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
ser.close()
