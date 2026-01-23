import cv2
import mediapipe as mp

# Initialize camera
cap = cv2.VideoCapture(0)

# MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Rectangle position
rect_x, rect_y = 200, 200
rect_size = 80

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Index finger tip (landmark 8)
            index_finger = hand_landmarks.landmark[8]
            x = int(index_finger.x * w)
            y = int(index_finger.y * h)

            # Move rectangle
            rect_x = x - rect_size // 2
            rect_y = y - rect_size // 2

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Draw rectangle
    cv2.rectangle(frame,
                  (rect_x, rect_y),
                  (rect_x + rect_size, rect_y + rect_size),
                  (0, 255, 0),
                  -1)

    cv2.imshow("Hand Controlled UI", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
