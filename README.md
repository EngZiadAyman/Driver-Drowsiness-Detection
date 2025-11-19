# 🚗💤 Driver Drowsiness Detection System

> **Status:** Production‑Ready Prototype • **Language:** Python • **Author:** Eng. Ziad Ayman

Welcome to the **Driver Drowsiness Detection System** — an AI‑powered solution designed to **save lives on the road** by detecting driver fatigue in real time using computer vision. Built with ❤️, tuned with precision, and crafted for real‑world safety.

---

## ✨ Overview

Fatigue is one of the leading causes of road accidents. This project provides a **real‑time drowsiness alert system** that tracks the driver’s eye state, head movement, and overall alertness using a standard webcam.

👉 When the system detects prolonged eye closure or abnormal head tilt, **an alarm is triggered instantly** to warn the driver.

---

## 🚀 Key Features

### 👁️ Real‑Time Eye Monitoring (EAR)

* Uses **Eye Aspect Ratio (EAR)** to detect long blinks & closed eyes.
* Highly accurate, efficient, and works well under different lighting conditions.

### 🧠 Head Pose Tracking

* Detects risky head movements: **Tilt, Nodding, Yawing**.
* Helps identify microsleep or loss of focus.

### 🔊 Smart Audio Alert

* Warning sound played in a separate thread.
* No lag, no frame freezing — smooth experience.

### 🖥️ Interactive On‑Screen HUD

* Live values for EAR, head rotation, and drowsiness state.
* Color indicators + status messages.

### ⚙️ Anti‑False Alarm Logic

* Alert triggers only after **30 consecutive frames** of drowsiness.
* Prevents false alarms from normal blinking.

---

## 📁 Project Structure

```
Driver-Drowsiness-Detection/
├─ detection/
│  ├─ face.py       # EAR calculation + eye landmarks
│  ├─ pose.py       # Head rotation angles
├─ main.py          # Main application loop
├─ state.py         # Drowsiness logic / state machine
├─ utils.py         # Helper functions
├─ requirements.txt
└─ README.md
```

---

## 🛠️ Requirements

* Python 3.8+
* OpenCV
* MediaPipe
* winsound (Windows only)

Install everything:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
git clone https://github.com/EngZiadAyman/Driver-Drowsiness-Detection.git
cd Driver-Drowsiness-Detection
pip install -r requirements.txt
python main.py
```

🎥 The webcam launches automatically.

---

## 🧮 Technical Breakdown

### 🔹 Eye Aspect Ratio (EAR)

EAR formula:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

If EAR < threshold for 30 frames ⇒ **Drowsy**.

### 🔹 Head Pose Estimation

Tracks:

* **Roll** (tilt)
* **Pitch** (nodding)
* **Yaw** (turning)

Values beyond the threshold = unsafe behavior.

### 🔹 Alarm Logic

* If state = Drowsy ➜ increase counter.
* If counter ≥ 30 ➜ 🔔 **Trigger alarm**.
* If driver reopens his eyes ➜ reset counter.

---

## 🔧 Adjustable Parameters

| Parameter               | Meaning                        | Default |
| ----------------------- | ------------------------------ | ------- |
| `earThresh`             | Minimum acceptable EAR         | 0.28    |
| `headThresh`            | Max allowed head tilt          | 6°      |
| `ALARM_FRAME_THRESHOLD` | Frames before triggering alarm | 30      |

Modify these inside `state.py` or `main.py`.

---

## 🌟 Future Improvements

* 📱 Mobile App or Web Dashboard
* ⚡ GPU acceleration
* 🔉 Cross‑platform audio alert
* 🧪 Deep Learning model for advanced fatigue detection
* 📸 Automatic snapshot on alert

---

## 🧩 Contributing

Contributions are welcome! 🙌

1. Fork the repo
2. Create a new branch
3. Commit your changes clearly
4. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**.

---

## 📬 Contact

For issues or collaboration, feel free to open a GitHub Issue.
