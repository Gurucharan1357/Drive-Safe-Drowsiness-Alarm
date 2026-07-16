# Drive-Safe-Drowsiness-Alarm

A real-time driver drowsiness detection system built with Python, OpenCV, and dlib. This project aims to prevent road accidents by monitoring the driver's eye movements and alertness levels, triggering an alarm if signs of drowsiness are detected.

---

## 📋 Project Overview
Driving while drowsy is a major cause of road accidents globally. **Drive-Safe-Drowsiness-Alarm** uses computer vision to track facial landmarks in real-time. By calculating the **Eye Aspect Ratio (EAR)**, the system determines whether the driver's eyes are closed for an extended period, triggering an audio alert to keep the driver awake.

## ✨ Key Features
*   **Real-Time Monitoring:** Processes video streams from your webcam instantly.
*   **Facial Landmark Detection:** Uses `dlib` to accurately pinpoint eye and facial structures.
*   **EAR Calculation:** Tracks eye closure duration to differentiate between a normal blink and actual drowsiness.
*   **Audio Alerts:** Automatically plays an alarm sound when the driver shows signs of fatigue.
*   **Lightweight & Efficient:** Optimized to run on standard hardware.

## 🛠️ Tech Stack
*   **Language:** Python 3.x
*   **Computer Vision:** OpenCV
*   **Facial Landmark Prediction:** dlib
*   **Numerical Computing:** NumPy
*   **Audio:** `pygame` or `playsound` (for the alarm)

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Gurucharan1357/Drive-Safe-Drowsiness-Alarm.git](https://github.com/Gurucharan1357/Drive-Safe-Drowsiness-Alarm.git)
   cd Drive-Safe-Drowsiness-Alarm

### Adjusting Sensitivity
You can tweak the threshold values inside `main.py` to change how sensitive the detection system is:
*   **`EAR_THRESHOLD`:** The value below which the eyes are considered "closed."
*   **`FRAME_CHECK`:** The number of consecutive frames the eyes must remain closed before the alarm triggers.

---

## ⚖️ Disclaimer
This project is intended strictly for educational and demonstration purposes. It should not be relied upon as a replacement for professional safety equipment or as a guarantee against vehicular accidents. Always prioritize safe driving practices.

## 🤝 Contributing
Contributions are welcome! If you find a bug or have an idea for an improvement (such as adding yawn detection or head pose estimation), feel free to fork the repository and submit a pull request.

---

## 👤 Author
**Gurucharan**
*   GitHub: [@Gurucharan1357](https://github.com/Gurucharan1357)
