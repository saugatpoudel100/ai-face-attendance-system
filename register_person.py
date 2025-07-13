import cv2, face_recognition, pathlib, sys
from flask import Flask
from database import db, Person

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
db.init_app(app)

with app.app_context():
    db.create_all()

CAPTURES = 5    # pictures per person

def capture(name):
    cam = cv2.VideoCapture(0)
    frames = []
    while len(frames) < CAPTURES:
        ok, frame = cam.read();  cv2.imshow("SPACE = capture / ESC = quit", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27: break       # ESC
        if key == 32:             # SPACE
            frames.append(frame.copy())
            print(f"[{len(frames)}/{CAPTURES}] captured")

    cam.release(); cv2.destroyAllWindows()
    return frames

def encode(frames):
    encs, blobs = [], []
    for f in frames:
        if f is None or f.size == 0:
            continue

        if f.dtype != "uint8":
            continue

        rgb = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)

        if rgb is None or rgb.shape[2] != 3:
            continue

        boxes = face_recognition.face_locations(rgb)
        if not boxes:
            continue

        enc = face_recognition.face_encodings(rgb, boxes)[0]
        encs.append(enc)

        _, buf = cv2.imencode('.jpg', f)
        blobs.append(buf.tobytes())

    return encs, blobs

if __name__ == "__main__":
    name = input("Person's name ➜ ").strip()
    if not name: sys.exit("Name cannot be empty!")

    with app.app_context():
        if Person.query.filter_by(name=name).first():
            sys.exit("Name already exists in DB!")

    frames = capture(name)
    encs, blobs = encode(frames)
    if not encs: sys.exit("No usable faces captured.")

    with app.app_context():
        p = Person(name=name, encodings=encs, images=blobs)
        db.session.add(p); db.session.commit()