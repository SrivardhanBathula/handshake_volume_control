# 🤝 Hand Gesture Volume Control

Control your system volume using just your hand!
This project uses **Computer Vision** to detect hand gestures and adjust volume in real time.

---

## 🚀 Features

* 🎥 Real-time hand tracking using webcam
* ✋ Control volume using thumb and index finger distance
* 🎚️ Smooth volume adjustment
* 📊 Visual volume bar with percentage
* 🔊 System volume control (Windows supported)
* ⚡ Fast and responsive

---

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Pycaw (for Windows volume control)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hand-gesture-volume-control.git
cd hand-gesture-volume-control
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

---

## ▶️ How to Run

```bash
python handshake_volume_control.py
```

---

## 🎮 How It Works

1. Show your hand to the webcam
2. Move your **thumb and index finger**:

   * 👌 Close → Low volume
   * ✋ Open → High volume
3. Press **'q'** to exit

---

## 🖥️ System Support

* ✅ Windows (full volume control using Pycaw)
* ⚠️ macOS / Linux → Only visual meter (no system volume control)

---

## 📁 Project Structure

```
.
├── handshake_volume_control.py
├── handshake_visual_volume.py
├── test_camera.py
├── README.md
```

---

## ⚠️ Notes

* Ensure your webcam is working
* Good lighting improves hand detection accuracy
* Keep your hand within camera frame

---

## 💡 Future Improvements

* 🔇 Mute gesture
* 🎛️ Control brightness
* 🖥️ GUI interface
* 🤖 Multi-hand support

