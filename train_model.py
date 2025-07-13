import os, pickle, pathlib
import face_recognition

DATASET_DIR = pathlib.Path("dataset")
ENCODINGS_PKL = pathlib.Path("face_encodings.pkl")

encodings, names = [], []

for person in DATASET_DIR.iterdir():
    if not person.is_dir(): continue
    for img_path in person.glob("*.*"):
        image = face_recognition.load_image_file(img_path)
        face_bboxes = face_recognition.face_locations(image)
        if not face_bboxes:
            continue
        enc = face_recognition.face_encodings(image, face_bboxes)[0]
        encodings.append(enc)
        names.append(person.name)

with open(ENCODINGS_PKL, "wb") as f:
    pickle.dump({"encodings": encodings, "names": names}, f)