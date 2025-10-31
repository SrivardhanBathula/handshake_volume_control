import cv2
import mediapipe as mp
import math
import numpy as np
import platform

# ---------------- Volume control imports ----------------
SYSTEM = platform.system().lower()
volume_iface = None

try:
    if SYSTEM == "windows":
        from ctypes import POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_iface = POINTER(IAudioEndpointVolume)(interface)
        vol_range = volume_iface.GetVolumeRange()
        VOL_MIN, VOL_MAX = vol_range[0], vol_range[1]
        print("✅ Volume control connected successfully!")
    else:
        raise Exception("Non-Windows system")
except Exception as e:
    print(f"⚠️ Volume control not available: {e}")
    volume_iface = None

# ---------------- Mediapipe setup ----------------
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands=1)

# ---------------- Webcam setup ----------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot open webcam.")
    exit()

print("🎥 Starting Handshake Volume Control...")
print("👉 Show your hand and move thumb + index finger to control volume")
print("👉 Press 'q' to quit")

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            h, w, _ = img.shape
            for id, lm in enumerate(handLms.landmark):
                lmList.append((int(lm.x * w), int(lm.y * h)))

            # Thumb tip (id=4), Index tip (id=8)
            x1, y1 = lmList[4]
            x2, y2 = lmList[8]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            # Convert length (30–200) to volume (0–100)
            vol_percent = np.interp(length, [30, 200], [0, 100])
            bar_height = np.interp(length, [30, 200], [400, 150])

            # Set system volume if available
            if volume_iface:
                level = VOL_MIN + (vol_percent / 100.0) * (VOL_MAX - VOL_MIN)
                volume_iface.SetMasterVolumeLevel(level, None)

            # Draw volume bar
            cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 255), 2)
            cv2.rectangle(img, (50, int(bar_height)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(vol_percent)} %', (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("🤝 Handshake Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("👋 Program ended safely.")
