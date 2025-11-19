
-----

## 🚗 Driver Drowsiness Detection System: Real-Time Fatigue Analysis

This project is a sophisticated **Computer Vision (CV)** solution designed to significantly enhance road safety by providing **real-time, non-intrusive monitoring** of the driver's alertness level. It leverages advanced facial landmark detection to identify critical fatigue indicators, primarily focusing on eye closure duration and head posture, ensuring immediate intervention when a threat is detected.

-----

## 🚀 Key Features and Technical Specifications

| Feature | Description | Technology Used |
| :--- | :--- | :--- |
| **Precision Drowsiness Detection** | Analyzes the **Eye Aspect Ratio (EAR)** to accurately measure the percentage of eye closure over time, the most reliable metric for fatigue. | `MediaPipe Face Mesh` |
| **Head Posture Monitoring** | Tracks the driver's **Head Pose** (Roll, Pitch, Yaw) to identify dangerous head nodding or significant distraction away from the road. | `MediaPipe Pose Estimation` |
| **30-Frame Activation Threshold** | The critical alarm is only triggered after **30 consecutive frames** of detected drowsiness, minimizing false alarms while ensuring prompt response. | **Custom Frame Counter Logic** |
| **Instant Audio Alert** | An immediate, intrusive sound alert is activated in a separate thread to guarantee the driver is roused without freezing the video stream. | `winsound` (Windows OS) & `threading` |
| **Real-Time Display** | Overlays current status (`Drowsy` or `Alert`), frame counter, and the visual warning on the live camera feed. | `OpenCV` (`cv2`) |

-----

## 🧐 In-Depth System Architecture and Logic

The system operates on a continuous loop, processing each video frame individually to derive crucial metrics.

### 1\. Facial Landmark Extraction (The Input Layer)

The project utilizes the powerful **MediaPipe Face Mesh** library to identify 468 3D facial landmarks per frame. From these landmarks, the system specifically targets those outlining the driver's eyes.

### 2\. Drowsiness Measurement: Eye Aspect Ratio (EAR)

  * **Calculation:** The **Eye Aspect Ratio (EAR)** is calculated by measuring the ratio between the vertical distance (eye openness) and the horizontal distance (eye width) of the eye landmarks.
    $$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2 \cdot ||p_1 - p_4||}$$
    *Where $p_1$ to $p_6$ are the coordinates of the eye landmarks.*
  * **Threshold:** A defined **EAR Threshold** (e.g., `earThresh = 0.28`) determines when an eye is considered 'closed'. When the calculated EAR drops below this value, the system registers a state of "potential drowsiness."

### 3\. Head Pose Estimation

The **MediaPipe Pose Estimation** module provides the angular orientation of the head in three axes:

  * **Roll:** Tilt along the nose axis (tilting the head to the left or right shoulder).
  * **Pitch:** Tilt up and down (nodding).
  * **Yaw:** Rotation left and right (looking away from the road).

These angles are compared against defined thresholds (`headThresh = 6` degrees) to detect dangerous movements indicating distraction or unconscious nodding.

### 4\. The 30-Frame Counter Logic (The Core Trigger)

This logic is crucial for distinguishing a natural blink from actual sleep:

  * **Counting:** If the `DriverState` evaluation (based on EAR and head pose) returns **"Drowsy"**, a dedicated variable (`consecutive_drowsy_frames`) is incremented.
  * **Reset:** If the state returns to **"Alert"** (even for a single frame), the counter is immediately reset to zero, ensuring the driver must maintain a sleepy state for the full duration.
  * **Trigger:** The alarm is activated only when:
    $$consecutive\_drowsy\_frames \geq 30$$

### 5\. Sound Alert Mechanism

Since direct sound playback in Python often leads to video freezing (lag), a robust solution is implemented:

  * **Library:** The built-in Windows library `winsound` is used for reliable, dependency-free audio output.
  * **Concurrency:** The alert function (`play_alarm_sound`) runs in a separate **Thread** (`threading` module). This ensures that the continuous **CV frame processing** in the main thread is never interrupted by the sound execution, maintaining high frame rates.
  * **State Control:** A global flag (`stop_alarm`) controls the sound loop. The loop continues to emit intermittent beeps until the driver's state becomes "Alert," at which point the flag is set to `True` and the sound thread terminates gracefully.

-----

## ⚙️ Installation and Execution

### 1\. Requirements

The project relies on standard Python Computer Vision libraries:

```bash
pip install opencv-python mediapipe
```

*(Note: `winsound` is a standard Windows library and requires no separate installation.)*

### 2\. Execution

To start the system, navigate to the project directory in your terminal and run:

```bash
python main.py
```

-----

## 👨‍💻 Project Structure (Code Detail)

The core functionality is distributed across several modules:

| File/Module | Description | Relevance to Drowsiness |
| :--- | :--- | :--- |
| `main.py` | The entry point. Handles video capture, sequential processing, frame counting, and the final alarm activation logic (`consecutive_drowsy_frames`). | Contains the core `while cap.isOpened()` loop and the final trigger logic. |
| `detection/face.py` | Calculates the **EAR**, detects blinking, and extracts the primary facial data used for the state evaluation. | Calculates the primary metric (EAR) for drowsiness. |
| `detection/pose.py` | Responsible for processing the image with MediaPipe and calculating the Roll, Pitch, and Yaw angles of the head. | Provides head position data to flag distraction/nodding. |
| `state.py` | Contains the `DriverState` class, which aggregates all metrics (EAR, Roll, Pitch, Yaw) and applies complex weighted logic to determine the final output state (`Drowsy` or `Alert`). | The decision-making engine of the system. |

-----

## 📝 License

This project is open-sourced under the **MIT License**.

-----

## 👤 Author

**Eng. Ziad Ayman**

  * [GitHub Profile](https://www.google.com/search?q=https://github.com/EngZiadAyman)
