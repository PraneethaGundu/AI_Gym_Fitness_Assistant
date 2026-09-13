import cv2

from pose_detector import PoseDetector
from squat_detector import SquatDetector, calculate_angle


def main():

    detector = PoseDetector()
    squat_detector = SquatDetector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Could not open camera.")
        return

    print("✅ Camera started.")
    print("🏋️ AI Squat Trainer started.")
    print("🧍 Stand sideways to the camera.")
    print("Press Q or ESC to quit.")

    while True:

        success, frame = camera.read()

        if not success:
            print("❌ Could not read camera frame.")
            break

        frame = cv2.flip(frame, 1)

        processed_frame, results = detector.detect(frame)

        if results.pose_landmarks:

            landmarks = results.pose_landmarks.landmark

            # --------------------------------
            # LEFT BODY LANDMARKS
            # --------------------------------

            shoulder = landmarks[11]
            hip = landmarks[23]
            knee = landmarks[25]
            ankle = landmarks[27]

            # Right knee for basic alignment
            right_knee = landmarks[26]

            h, w, _ = frame.shape

            shoulder_point = (
                int(shoulder.x * w),
                int(shoulder.y * h)
            )

            hip_point = (
                int(hip.x * w),
                int(hip.y * h)
            )

            knee_point = (
                int(knee.x * w),
                int(knee.y * h)
            )

            ankle_point = (
                int(ankle.x * w),
                int(ankle.y * h)
            )

            right_knee_point = (
                int(right_knee.x * w),
                int(right_knee.y * h)
            )

            # --------------------------------
            # KNEE ANGLE
            # --------------------------------

            knee_angle = calculate_angle(
                hip_point,
                knee_point,
                ankle_point
            )

            # --------------------------------
            # BACK POSTURE ANGLE
            # --------------------------------

            back_angle = calculate_angle(
                shoulder_point,
                hip_point,
                knee_point
            )

            # --------------------------------
            # KNEE ALIGNMENT
            # --------------------------------

            knee_difference = abs(
                knee.x - right_knee.x
            )

            knee_alignment = knee_difference > 0.12

            # --------------------------------
            # UPDATE SQUAT
            # --------------------------------

            reps, stage = squat_detector.update(
                knee_angle
            )

            # --------------------------------
            # FEEDBACK
            # --------------------------------

            feedback = squat_detector.get_form_feedback(
                knee_angle,
                back_angle,
                knee_alignment
            )

            score = squat_detector.calculate_score(
                knee_angle,
                back_angle,
                knee_alignment
            )

            # --------------------------------
            # DISPLAY
            # --------------------------------

            cv2.putText(
                processed_frame,
                f"Reps: {reps}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )

            cv2.putText(
                processed_frame,
                f"Knee: {int(knee_angle)} deg",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                processed_frame,
                f"Back: {int(back_angle)} deg",
                (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                processed_frame,
                f"Stage: {stage}",
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                processed_frame,
                f"Score: {score}/100",
                (20, 185),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # --------------------------------
            # FORM FEEDBACK
            # --------------------------------

            y = 230

            for message in feedback:

                cv2.putText(
                    processed_frame,
                    message,
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 255),
                    2
                )

                y += 32

        else:

            cv2.putText(
                processed_frame,
                "No person detected",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # --------------------------------
        # SHOW WINDOW
        # --------------------------------

        cv2.imshow(
            "AI Gym Trainer - Full Squat Analysis",
            processed_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            break

    camera.release()
    detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()