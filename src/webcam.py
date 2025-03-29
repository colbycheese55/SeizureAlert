import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_upperbody = mp.solutions.pose
mp_face = mp.solutions.face_mesh

hands = mp_hands.Hands()
upperbody = mp_upperbody.Pose()
face = mp_face.FaceMesh()
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
    face_results = face.process(rgb_frame)

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Draw face landmarks
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_draw.draw_landmarks(frame, face_landmarks, mp_face.FACEMESH_TESSELATION)

    # Draw pose landmarks (includes neck & shoulders)
    if upperbody_results.pose_landmarks:
        mp_draw.draw_landmarks(frame, upperbody_results.pose_landmarks, mp_upperbody.POSE_CONNECTIONS)

    # Display the frame
    cv2.imshow("MediaPipe Hand, Face, and Upperbody", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
