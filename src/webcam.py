import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import mediapipe as mp
import sys
import time
import ui

# Seizure detection settings
SEIZURE_THRESHOLD = 2  # Movement level required to trigger an alert (% of screen)
ACCELERATION_THRESHOLD = 1  # Required acceleration to detect sudden movements
DURATION_THRESHOLD = 1  # Required duration in seconds
HISTORY_LENGTH = 15 # Frames to track (~3 seconds if running at 10 FPS)
MOVEMENT_HISTORY = []
ACCELERATION_HISTORY = []
ALERT_TRIGGERED = False

# MediaPipe initialization
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

class Worker(QThread):
    update_signal = pyqtSignal(QImage)
    movement_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # Start capturing from the first webcam
        self.previous_frame = None
        self.hands = mp_hands.Hands()
        self.pose = mp_pose.Pose()
        self.face_mesh = mp_face.FaceMesh()
        self.start_time = None  # Timer for seizure detection

    def process_frame(self):
        """Captures frame, detects movement, and calculates movement level with MediaPipe overlays."""
        ret, frame = self.cap.read()
        if not ret:
            return None, 0
        
        frame = cv2.resize(frame, (1000, 750))

        # Convert to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame for hand, pose, and face landmarks
        hand_results = self.hands.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        face_results = self.face_mesh.process(rgb_frame)

        # Draw hand landmarks on the frame
        if hand_results.multi_hand_landmarks:
            for hand in hand_results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        
        # Draw pose landmarks on the frame
        if pose_results.pose_landmarks:
            mp_draw.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Draw face landmarks on the frame
        if face_results.multi_face_landmarks:
            for face in face_results.multi_face_landmarks:
                mp_draw.draw_landmarks(frame, face, mp_face.FACEMESH_TESSELATION)

        # Convert frame to grayscale for movement detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
            return frame, 0

        frame_diff = cv2.absdiff(self.previous_frame, gray)
        self.previous_frame = gray

        movement_level = np.sum(frame_diff > 15) / frame_diff.size * 100  # Threshold for subtle movements
        return frame, movement_level

    def detect_seizure(self, movement):
        """Detects consistent small movements over time with acceleration check."""
        global ALERT_TRIGGERED

        MOVEMENT_HISTORY.append(movement)
        if len(MOVEMENT_HISTORY) > HISTORY_LENGTH:
            MOVEMENT_HISTORY.pop(0)

        # Calculate acceleration
        if len(MOVEMENT_HISTORY) > 1:
            acceleration = abs(MOVEMENT_HISTORY[-1] - MOVEMENT_HISTORY[-2])
            ACCELERATION_HISTORY.append(acceleration)
            if len(ACCELERATION_HISTORY) > HISTORY_LENGTH:
                ACCELERATION_HISTORY.pop(0)
        else:
            acceleration = 0

        # Start timing if movement is consistently above threshold
        if movement >= SEIZURE_THRESHOLD:
            if self.start_time is None:
                self.start_time = time.time()  # Start timer

            # Keep track of how long movement is above the threshold
            elapsed_time = time.time() - self.start_time

            if elapsed_time >= DURATION_THRESHOLD:
                THRESHOLD_RATIO = 0.75
                if sum(a >= ACCELERATION_THRESHOLD for a in ACCELERATION_HISTORY[-HISTORY_LENGTH:]) >= THRESHOLD_RATIO * HISTORY_LENGTH:
                    if not ALERT_TRIGGERED:
                        ALERT_TRIGGERED = True
                        print("🚨 Seizure detected! 🚨")
                        ui.alert_text = 'Seizure stimulus detected! Do you need help?'
                        ui.seizure.set()

        else:
            # Introduce a grace period before resetting the timer
            if self.start_time is not None and time.time() - self.start_time > 3:  # 3-second grace period
                self.start_time = None
                ALERT_TRIGGERED = False

    def run(self):
        while True:
            frame, movement = self.process_frame()

            if frame is None:
                continue

            self.detect_seizure(movement)

            # Convert frame to QImage for display in PyQt5
            height, width, channels = frame.shape
            bytes_per_line = channels * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

            self.update_signal.emit(q_img)  # Emit signal to update the UI
            self.movement_signal.emit(movement)

    def stop(self):
        self.cap.release()

class SeizureAlertApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seizure Alert System")
        self.setGeometry(400, 400, 800, 600)

        # Layout for the window
        self.layout = QVBoxLayout()

        # Video label
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Movement level label
        self.movement_label = QLabel("Movement Level: 0%", self)
        self.layout.addWidget(self.movement_label)

        # Seizure alert label
        self.alert_label = QLabel("🚨 SEIZURE ALERT! 🚨", self)
        self.alert_label.setStyleSheet("color: red; font-size: 20px; font-weight: bold;")
        self.alert_label.setAlignment(Qt.AlignCenter)
        self.alert_label.hide()  # Hide initially
        self.layout.addWidget(self.alert_label)

        # Initialize worker and connect signals
        self.worker = Worker()
        self.worker.update_signal.connect(self.update_video_feed)
        self.worker.movement_signal.connect(self.update_movement_label)

        self.setLayout(self.layout)

    def start_webcam(self):
        """Start the webcam feed in a separate thread."""
        self.worker.start()  # Start the worker thread for webcam feed and processing

    def update_video_feed(self, q_img):
        """Updates the video feed in the GUI"""
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)

    def update_movement_label(self, movement):
        """Updates the movement label and shows alert if needed"""
        self.movement_label.setText(f"Movement Level: {movement:.2f}%")

        if ALERT_TRIGGERED:
            self.alert_label.show()
        else:
            self.alert_label.hide()

    def closeEvent(self, event):
        """Handle window close event"""
        self.worker.stop()
        event.accept()

# def start_webcam():
#     """Start the webcam GUI in a separate thread."""
#     app = QApplication(sys.argv)
#     window = SeizureAlertApp()
#     window.show()
#     window.start_webcam()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     start_webcam()




