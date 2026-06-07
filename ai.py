import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

count = 0

while True:
    success, img = cap.read()

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = pose.process(img_rgb)

    if results.pose_landmarks:

        mp_draw.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[11].y
        left_elbow = landmarks[13].y

        if left_elbow > left_shoulder:
            count += 1

        cv2.putText(
            img,
            f'Pushups: {count}',
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            3
        )

    cv2.imshow("FitFlex AI", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()