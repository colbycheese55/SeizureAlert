import cv2
import mediapipe as mp
import numpy as np
import torch
import csv
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_upperbody = mp.solutions.pose
mp_face = mp.solutions.face_mesh

hands = mp_hands.Hands()
upperbody = mp_upperbody.Pose()
face_mesh = mp_face.FaceMesh()
mp_draw = mp.solutions.drawing_utils

# Initialize Webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

open("../data/landmarks_data.csv", "w").close()

csv_file = open("../data/landmarks_data.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp", "type", "index", "x", "y", "z"])  # Header

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
    upperbody_results = upperbody.process(rgb_frame)
    face_results = face_mesh.process(rgb_frame)

    current_time = time.time()

    # Save Hand Landmarks
    if hand_results.multi_hand_landmarks:
        for hand in hand_results.multi_hand_landmarks:
            for idx, lm in enumerate(hand.landmark):
                csv_writer.writerow([current_time, "hand", idx, lm.x, lm.y, lm.z])
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # Save Face Landmarks
    if face_results.multi_face_landmarks:
        for face in face_results.multi_face_landmarks:
            for idx, lm in enumerate(face.landmark):
                csv_writer.writerow([current_time, "face", idx, lm.x, lm.y, lm.z])
            mp_draw.draw_landmarks(frame, face, mp_face.FACEMESH_TESSELATION)

    # Save Pose Landmarks
    if upperbody_results.pose_landmarks:
        for idx, lm in enumerate(upperbody_results.pose_landmarks.landmark):
            csv_writer.writerow([current_time, "pose", idx, lm.x, lm.y, lm.z])
        mp_draw.draw_landmarks(frame, upperbody_results.pose_landmarks, mp_upperbody.POSE_CONNECTIONS)

    # Display the frame
    cv2.imshow("MediaPipe Hand, Face, and Upperbody", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
