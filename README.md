# TouchlessMouse V1.0

*[Versión en Español](README.es.md)*

Control your computer cursor through gestures and computer vision, without needing to touch the physical mouse.

## Requirements
- **Python 3.10** or higher.
- A **Webcam** connected.

---

## Linux (Installation and Execution)

1. **Open terminal** in the project folder.
2. **Create virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   ```
3. **Activate environment**:
   ```bash
   source venv/bin/activate
   ```
4. **Install dependencies**:
   ```bash
   pip install opencv-python mediapipe pyautogui sounddevice numpy
   ```
5. **Run**:
   ```bash
   python main.py
   ```

---

## Windows (Installation and Execution)

1. **Open CMD or PowerShell** in the project folder.
2. **Create virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```
3. **Activate environment**:
   ```bash
   venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install opencv-python mediapipe pyautogui sounddevice numpy
   ```
5. **Run**:
   ```bash
   python main.py
   ```
   
---

## Commands 

1. **Move cursor**: Raise your index finger, it will light up in green and you can drag. (High sensitivity)

2. **Click and Precision Mode**: While raising your index, raise your pinky finger and it will light up in red, lower and raise the pinky quickly and you will click. (Low sensitivity)

3. **Hold click to drag**: While dragging the cursor, raise your middle finger and it will light up in orange, keep it extended for a moment and it will light up in blue, now the click is held, allowing scrolling.

4. **"Stop!"**: Open your hand completely and the system will stop completely. (All fingers will light up)

**Consideration**: Lighting can influence the interpretation of multiple combinations, it is recommended to configure specific attributes in **config.py**.

---

## Configuration

- Camera resolution and FPS limitation
- Hand detection sensitivity
- Gesture activation thresholds
- Cursor sensitivity
- Debug window configuration

**Note**: The program modules can be improved and might need their own configurations.

---

## License

MIT License - See **LICENSE** for more details.

## Contributions

Feel free to comment or make pull requests for improvements!
