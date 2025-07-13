from flask import Flask, Response, render_template, request, jsonify
from camera import VideoCamera
from recognize import FaceRecognizer
from database import db, Attendance
import cv2

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

cam = None
face = None
last_recognized_names = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    def stream():
        global last_recognized_names
        while True:
            frame = cam.frame()
            if frame is None:
                continue
            frame, names = face.annotate_and_log(frame)
            last_recognized_names = names  # Update globally
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/get_names")
def get_names():
    # Returns JSON list of last recognized names
    return jsonify({"names": list(set(last_recognized_names))})

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    data = request.json
    name = data.get("name")
    mark_type = data.get("type")
    if not name or mark_type not in ("Entry", "Exit"):
        return jsonify({"error": "Invalid data"}), 400

    success = Attendance.mark(name, mark_type)
    if success:
        return jsonify({"message": f"{mark_type} marked for {name}"}), 200
    else:
        return jsonify({"error": f"Failed to mark {mark_type} for {name}"}), 400

@app.route("/attendance")
def attendance():
    rows = Attendance.query.order_by(Attendance.date.desc(), Attendance.name).all()
    return render_template("attendance.html", rows=rows)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        cam = VideoCamera()
        face = FaceRecognizer(app, tolerance=0.5)
    app.run(debug=True)