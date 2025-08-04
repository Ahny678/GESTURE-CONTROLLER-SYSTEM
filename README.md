# 🖐️ Gesture Controller System

## Control Volume, Brightness, Screenshots, and Voice Recording — All with Hand Gestures

---

### 🎯 Introduction

The **Gesture Controller System** is a Python-based computer vision application that allows users to control **system volume**, **screen brightness**, **take screenshots**, and **record spoken audio** — **all through simple hand gestures** using a webcam. Built using **MediaPipe**, **OpenCV**, and modules like **PyCaw**, **PyAudio**, and **Vosk**, this system provides an intuitive, hands-free interface for everyday computer interactions. If you're searching for a **hand gesture Python project**, **gesture-based UI**, or **computer vision automation**, this project hits the mark.

---

### 🧠 How It Works (Modes & Diagram)

The system operates by recognizing specific left-hand gestures to activate one of four modes. The right hand then performs the associated function.

```
+----------------------------+------------------------------------------+
|  Gesture (Left Hand)       |  Mode Activated(Right Hand)                          |
+----------------------------+------------------------------------------+
| Index Finger Up           | Volume Adjustment(thumb+index: distance) |
| Index + Middle Finger     | Brightness Adjustment(ditto)             |
| Index + Middle + Ring     | Screenshot(thumb+index: gesture trigger) |
| All Fingers Up            | Voice Recorder (speech-to-text)          |
+----------------------------+------------------------------------------+
```

**📷 Camera Feed > 🤖 MediaPipe HandLandmarks > 🧠 Custom Logic > ⚙️ OS Action**

* **MediaPipe** detects both hands and tracks key landmarks.
* **Custom logic** in `Ahnytracker.py` extracts relevant points.
* **Controller logic** in `controller.py` interprets gestures and executes system commands.

---

### 🧰 Installation (For Users)

> ✅ Requirements: Python 3.8+, a webcam, and a Windows environment.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/gesture-controller-system.git
   cd gesture-controller-system
   ```

2. **Create a virtual environment** *(optional but recommended)*:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Vosk model**:

   * Download the model from: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
   * Unzip it into the project directory and rename it `vosk-model`.

5. **Run the controller**:

   ```bash
   python controller.py
   ```

---

### 🛠️ Installation (For Developers/Contributors)

In addition to the user steps:

6. **Structure Overview**:

   ```
   .
   ├── Ahnytracker.py          # Custom MediaPipe hand tracker
   ├── controller.py           # Main logic for all modes
   ├── spoken_words.txt        # Output of voice recording mode
   └── vosk-model/             # Vosk model directory
   ```

7. **Dev Dependencies** (example `requirements.txt`):

   ```
   opencv-python
   mediapipe
   numpy
   pycaw
   pyautogui
   screen-brightness-control
   vosk
   pyaudio
   comtypes
   ```

---

### 🤝 Contributor Expectations

We welcome contributions! Here’s what we expect:

* Stick to PEP8 formatting.
* Keep code modular and document functions.
* Open a detailed issue or feature request before submitting a PR.
* Comment your code, especially in the gesture recognition logic.
* Respect the logic separation: `Ahnytracker.py` (hand tracking) vs `controller.py` (mode handling).

---

### 🧩 Known Issues & Limitations

* ❗ **Platform limitation**: Screen brightness control and PyCaw only work on Windows.
* 🧠 **Gesture accuracy**: Inconsistent detection under poor lighting or fast movement.
* 🎤 **Audio overflow**: Vosk may drop input if the microphone buffer overflows.
* 📷 **Webcam resolution**: Lower resolutions may affect gesture tracking accuracy.
* 📁 **Hardcoded file names**: E.g., `spoken_words.txt` and `screenshot.png` are fixed.
