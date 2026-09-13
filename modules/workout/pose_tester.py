import cv2

from pose_detector import PoseDetector


def main():
    detector = PoseDetector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Could not open camera.")
        return

    print("✅ Camera started.")
    print("🧍 Stand in front of the camera.")
    print("Press Q or ESC to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("❌ Could not read camera frame.")
            break

        frame = cv2.flip(frame, 1)

        processed_frame, results = detector.detect(frame)

        cv2.imshow(
            "AI Gym Trainer - Pose Detection",
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