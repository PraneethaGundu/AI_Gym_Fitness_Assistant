import cv2
import mediapipe as mp


class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, frame):
        """
        Detect human body landmarks from a camera frame.

        Returns:
            processed_frame: Frame with pose landmarks drawn.
            results: MediaPipe pose detection results.
        """

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.pose.process(rgb_frame)

        processed_frame = frame.copy()

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                processed_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return processed_frame, results

    def close(self):
        self.pose.close()