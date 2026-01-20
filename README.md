# TouchlessMouse V1.1

*[Versión en Español](README.es.md)*

Control your computer cursor through gestures and computer vision, without needing to touch the physical mouse.

## What's New in v1.1

**New Features**
- **Right Click**: Ring finger extended activates right click.
- **Dynamic Hand Detection**: White circle indicator on wrist when hand is closed.
- **Single Hand Tracking**: When fully opened, system locks to that hand (eliminates cross-hand detection).

**Improvements**
- **Visual Feedback Enhancements**: Improved finger indicators (colors, sizes, and timing).
- **Performance Improvements**: Removed unnecessary processes like lighting processing.
- **Cursor Stabilizer**: Added a momentary freeze when exiting Precision Mode to prevent cursor jumps.
- **Anatomical Assist**: Algorithm to infer Ring finger position when partially occluded by the Pinky.

---

## Requirements
- **Python 3.10** or higher
- A **Webcam** connected

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

### Hand Selection
**Lock/Unlock hand**: Your closed fists will show a **white circle** on the wrist. Open the hand you want to use completely - this will lock that hand for tracking. To unlock, simply close the fist again.

### Cursor Control
1. **Move cursor**: Raise your index finger (lights up **Green**) to drag the cursor with high sensitivity.

2. **Click and Precision Mode**: While raising your index, raise your pinky finger (lights up **Red**). To **click**, quickly retract and extend the pinky again (double-tap gesture).

3. **Hold click to drag**: While dragging the cursor, raise your middle finger (lights up **Orange**). Keep it extended for a moment until it turns **Blue** - now click is held, allowing drag & scroll.

### Right Click (Two Methods)
- **Method 1**: Raise your ring finger alone (lights up **Orange**), hold briefly until **Blue** for right click.
- **Method 2 (Ergonomic)**: Raise middle + ring fingers together (4 fingers max)

### Emergency Stop
**"Stop!"**: Open your hand completely - all fingers light up **Red** and the system pauses.

**Consideration**: Lighting conditions can affect gesture recognition. Adjust parameters in **config.py** for optimal performance.

---

## Configuration (`config.py`)

Customize system behavior by modifying these key parameters:

### Camera Settings
- `FRAME_WIDTH` / `FRAME_HEIGHT`: Resolution (default 640x480 for better precision)
- `FPS_TARGET`: Capture speed

### Detection
- `MIN_DETECTION_CONFIDENCE`: Detection threshold
- `MODEL_COMPLEXITY`: 0 (Fast) or 1 (Accurate, default)

### Movement
- `SENSITIVITY`: Cursor speed
- `SMOOTHING_FACTOR`: Reduces hand shake/jitter

### Gestures
- `PINKY_TRIGGER_RATIO`: Click sensitivity
- `DRAG_ACTIVATION_TIME`: Hold time before drag activates

### Debug
- `SHOW_DEBUG_WINDOW`: Enable/disable visual feedback window

**Note**: Individual modules can be further customized for specific needs.

---

## Changelog

### v1.1 (January 20, 2026)
- Dynamic dual-hand detection with visual wrist indicators.
- Single active hand tracking system (prevents interference).
- Right click: ring finger extended.
- Alternative right click: middle + ring (ergonomic 4-finger mode).
- Enhanced visual feedback for hand states.
- Performance optimizations.

### v1.0 (Initial Release)
- Basic cursor control via index finger.
- Click functionality with pinky.
- Drag-and-hold with middle finger.
- Emergency stop gesture.
- Configurable sensitivity and smoothing.

---

## License

MIT License - See **LICENSE** for details.

## Contributions

Feel free to open issues or submit pull requests for improvements!
