'''
Hand detection algorithm
With openCV and mediapipe
The camera record through webcam, recognize the movement and return the last hand gesture identified
'''

import cv2
import mediapipe as mp

def hand_recognition():
    # Initialize mediapipe hands
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    # Start capturing video
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame and detect hands
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get landmark positions
                landmarks = hand_landmarks.landmark

                # Get tip of thumb and tip of index finger
                thumb_tip = landmarks[4]
                index_tip = landmarks[8]
                middle_tip = landmarks[12]
                ring_tip = landmarks[16]
                pinky_tip = landmarks[20]
                wrist = landmarks[0]

                # Convert to pixel coordinates
                h, w, _ = frame.shape
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                middle_x, middle_y = int(middle_tip.x * w), int(middle_tip.y * h)


                # Gesture Recognition
                # if thumb_y < wrist.y and index_y < wrist.y:  # Hand fully open
                #     gesture = "Open Hand"
                if abs(thumb_x - index_x) > 30 and abs(thumb_y - index_y) > 30 and abs(middle_x - index_x) > 30 and abs(middle_y - index_y) > 30  :  # Fingers touching
                    gesture = "Open hand"

                # elif thumb_x < index_x:  # Thumb up
                #     gesture = "Thumbs Up"
                elif thumb_y < index_y:  # Thumb up
                    gesture = "Thumbs Up"
                elif abs(thumb_x - index_x) < 30 and abs(thumb_y - index_y) < 30:  # Fingers touching
                    gesture = "Pinching"
                else:
                    gesture = "Unknown"

                # Display gesture on screen
                cv2.putText(frame, f'Gesture: {gesture}', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the output
        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

    # return the last movement executed
    return gesture


hand_recognition()