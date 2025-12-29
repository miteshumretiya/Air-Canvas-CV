# Air Canvas – Hand Gesture Drawing Using OpenCV

Air Canvas is a real-time computer vision application that enables users to draw on a virtual canvas using hand gestures captured through a webcam. The project uses OpenCV for video processing and MediaPipe Hands for accurate hand landmark detection.

This application demonstrates practical implementation of gesture recognition, real-time image processing, and human–computer interaction using Python.

---

## Project Overview

Air Canvas removes the need for traditional input devices such as a mouse or touchscreen by allowing users to draw in mid-air using hand movements. The index finger is tracked and used as a drawing tool, while different hand gestures are used to switch between drawing modes and tools.

The system processes live webcam input, detects hand landmarks, and renders drawings on a virtual canvas that is overlaid on the video feed in real time.

---

## Features

* Real-time hand tracking using MediaPipe Hands
* Gesture-based drawing without physical input devices
* Index finger tracking for drawing
* Mode switching using finger gestures
* Multiple brush colors:

  * Red
  * Green
  * Blue
  * Yellow
* Eraser tool for clearing drawings
* Persistent canvas overlay
* Adjustable brush and eraser thickness

---

## Technologies Used

* Python 3
* OpenCV
* MediaPipe
* NumPy

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/miteshumretiya/Air-Canvas-CV.git
cd Air-Canvas-CV
```

### 2. Install Required Libraries

```bash
pip install opencv-python mediapipe numpy
```

---

## Running the Application

```bash
python air_canvas.py
```

Make sure a webcam is connected and not being used by any other application. Adequate lighting is required for accurate hand detection.

---

## Gesture Controls

### Selection Mode

* Raise **index finger and middle finger**
* Move the hand to the top toolbar
* Select a brush color or the eraser

### Drawing Mode

* Raise **only the index finger**
* Move the finger to draw on the canvas
* Uses the currently selected brush or eraser

---

## Configuration

The following parameters can be adjusted in the source code to customize the drawing experience:

```python
brush_size = 15
eraser_size = 50
draw_color = (255, 0, 255)
```

---

## Requirements

* Python 3.8 or higher
* Webcam
* Good lighting conditions
* Single visible hand (application is designed for one-hand tracking)


## License

This project is open-source and intended for educational and personal use.

---

## Acknowledgements

* OpenCV
* MediaPipe
