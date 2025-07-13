import cv2

class VideoCamera:
    def __init__(self, src=0):
        self.cam = cv2.VideoCapture(src)
        if not self.cam.isOpened():
            raise RuntimeError("❌ Unable to open video source")
        else:
            print("✅ Camera opened successfully")

    def __del__(self):
        if self.cam.isOpened():
            self.cam.release()

    def frame(self):
        ok, frame = self.cam.read()
        if not ok:
            print("⚠️ Camera read failed")
            return None
        return frame
