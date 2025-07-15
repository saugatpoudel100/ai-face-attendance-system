# AI Face Attendance System

A real-time face recognition attendance system built with Python, OpenCV, Flask, and SQLite.  
This system captures video from your webcam, recognizes registered faces, and logs attendance automatically with entry and exit timestamps.

---

## Features

- Real-time face detection and recognition using OpenCV and the face_recognition library  
- Attendance marking with Entry and Exit types  
- Web-based interface powered by Flask  
- Stores attendance records in SQLite database  
- Live video streaming on a web page  
- Dashboard to view attendance history  

---

## Requirements

- Python 3.7+  
- OpenCV  
- Flask  
- face_recognition  
- Flask-SQLAlchemy  
- SQLite (built-in with Python)  

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/saugatpoudel100/ai_face_attendance_system.git
    cd ai_face_attendance_system
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Prepare your dataset folder:

    - Create a `dataset/` directory in the project root.  
    - Add subfolders named after each person (e.g., `dataset/John/`) containing their face images.

5. Train the model (if applicable):

    ```bash
    python train_model.py
    ```

---

## Usage

1. Run the Flask app:

    ```bash
    python app.py
    ```

2. Open your browser and visit:

    ```
    http://localhost:5000/
    ```

3. The webcam feed should appear. When recognized faces are detected, their names will show and attendance can be marked.

4. Navigate to the attendance page to see logged records.

---

## Project Structure

```plaintext
ai_face_attendance_system/
├── app.py               # Flask app main file
├── camera.py            # Webcam video capture class
├── recognize.py         # Face recognition and annotation logic
├── train_model.py       # Script to train face encodings from dataset
├── database.py          # Database models and functions (SQLite)
├── attendance.db        # SQLite database file (auto-generated)
├── dataset/             # Folder containing face images (organized by person)
├── templates/           # HTML templates for Flask routes
│   ├── index.html
│   └── attendance.html
├── static/              # Static assets like CSS, JS (optional)
├── requirements.txt     # Python dependencies
└── README.md            # This file
Troubleshooting
```
---
## Camera not opening:
Check if your webcam is connected and accessible. Try running a standalone OpenCV camera test.

## Face recognition errors:
Make sure the images in dataset/ are clear face pictures. Also ensure frames are converted from BGR to RGB before recognition.

## No video feed on web page:
Confirm the video feed route /video_feed is working and your browser allows webcam access.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
OpenCV for computer vision tools

face_recognition library by Adam Geitgey

Flask web framework

Inspired by various open source face attendance projects

