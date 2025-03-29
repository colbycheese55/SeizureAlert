import cv2
import mediapipe as mp
import numpy as np
import torch

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

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
    upperbody_results = upperbody.process(rgb_frame)
    face_results = face_mesh.process(rgb_frame)

    # Draw and extract hand landmarks
    if hand_results.multi_hand_landmarks:
        hand_landmarks = []
        for hand in hand_results.multi_hand_landmarks:
            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            # Convert to array
            hand_landmarks.append([[lm.x, lm.y, lm.z] for lm in hand.landmark])
        hand_array = np.array(hand_landmarks)  # Convert to NumPy
        print("Hand Landmarks:\n", hand_array.shape)
        print("Hand as Tensor:\n", torch.tensor(hand_array))  # Convert to Tensor

    # Draw and extract face landmarks
    if face_results.multi_face_landmarks:
        face_landmarks = [[lm.x, lm.y, lm.z] for lm in face_results.multi_face_landmarks[0].landmark]
        face_array = np.array(face_landmarks)  # Convert to NumPy
        # Draw landmarks
        for face in face_results.multi_face_landmarks:
            mp_draw.draw_landmarks(frame, face, mp_face.FACEMESH_TESSELATION)
        print("Face Landmarks:\n", face_array.shape)
        print("Face as Tensor:\n", torch.tensor(face_array))  # Convert to Tensor

    # Draw and extract pose landmarks (neck included)
    if upperbody_results.pose_landmarks:
        pose_landmarks = [[lm.x, lm.y, lm.z] for lm in upperbody_results.pose_landmarks.landmark]
        pose_array = np.array(pose_landmarks)  # Convert to NumPy
        # Draw landmarks
        mp_draw.draw_landmarks(frame, upperbody_results.pose_landmarks, mp_upperbody.POSE_CONNECTIONS)
        print("Pose Landmarks:\n", pose_array.shape)
        print("Pose as Tensor:\n", torch.tensor(pose_array))  # Convert to Tensor

    # Display the frame
    cv2.imshow("MediaPipe Hand, Face, and Upperbody", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
