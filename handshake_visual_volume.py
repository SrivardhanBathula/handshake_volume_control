import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize Mediapipe Hand Detection
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

# Function to map one range to another
def interp(val, in_min, in_max, out_min, out_max):
    return np.interp(val, [in_min, in_max], [out_min, out_max])

print("🎥 Starting Handshake Digital Volume Meter...")
print("👉 Move thumb and index finger to change volume.")
print("👉 Press 'q' to quit.")

# Variables
prev_volume = 0
smooth_volume = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    h, w, c = img.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Thumb tip (4) and Index tip (8)
            thumb_x, thumb_y = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
            index_x, index_y = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

            # Draw markers
            cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 0), 3)

            # Distance between fingers
            length = math.hypot(index_x - thumb_x, index_y - thumb_y)
            volume = int(interp(length, 30, 200, 0, 100))
            volume = int(np.clip(volume, 0, 100))

            # Smooth transition
            smooth_volume = int(0.8 * smooth_volume + 0.2 * volume)

            # Color based on volume
            if smooth_volume < 40:
                color = (0, 255, 0)
            elif smooth_volume < 75:
                color = (0, 255, 255)
            else:
                color = (0, 0, 255)

            # Digital meter bar
            meter_start = 150
            meter_end = 600
            fill = int(interp(smooth_volume, 0, 100, meter_start, meter_end))
            cv2.rectangle(img, (meter_start, 50), (meter_end, 100), (255, 255, 255), 2)
            cv2.rectangle(img, (meter_start, 50), (fill, 100), color, cv2.FILLED)

            # Volume text
            cv2.putText(img, f"{smooth_volume}%", (meter_end + 30, 90),
                        cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)

            # Label
            cv2.putText(img, "Volume Meter", (meter_start, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

    cv2.imshow("Handshake Digital Volume Meter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("👋 Program ended safely.")

