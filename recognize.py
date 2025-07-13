# recognize.py
import face_recognition
import cv2
import time
from database import Person, Attendance

class FaceRecognizer:
    def __init__(self, app, tolerance=0.5, reload_secs=30):
        self.app = app
        self.tol = tolerance
        self.reload_secs = reload_secs
        self._load_from_db()

    def _load_from_db(self):
        with self.app.app_context():
            self.known_enc, self.known_names = Person.all_encodings()
        self._last_reload = time.time()

    def maybe_reload(self):
        if time.time() - self._last_reload > self.reload_secs:
            self._load_from_db()

    def annotate_and_log(self, frame):
        self.maybe_reload()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for (top, right, bottom, left), enc in zip(boxes, encodings):
            matches = face_recognition.compare_faces(self.known_enc, enc, tolerance=self.tol)
            name = "Unknown"
            if True in matches:
                idx = matches.index(True)
                name = self.known_names[idx]
                names.append(name)
                with self.app.app_context():
                    Attendance.mark(name, "Entry")  # Or handle marking outside for user choice
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        return frame, names