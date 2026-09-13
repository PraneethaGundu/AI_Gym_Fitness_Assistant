import math


def calculate_angle(point1, point2, point3):
    """
    Calculate the angle formed by three points.
    point2 is the vertex.
    """

    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    angle = math.degrees(
        math.atan2(y3 - y2, x3 - x2)
        - math.atan2(y1 - y2, x1 - x2)
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


class SquatDetector:

    def __init__(self):

        self.reps = 0
        self.stage = "up"

        self.good_depth_reps = 0
        self.shallow_reps = 0

        self.min_angle = 180

    def update(self, knee_angle):

        # ----------------------------------------------------
        # DOWN POSITION
        # ----------------------------------------------------
        # 120 degrees is more suitable for beginner squats.
        # We still use 100 degrees to classify good depth.

        if knee_angle < 120:

            if knee_angle < self.min_angle:
                self.min_angle = knee_angle

            self.stage = "down"

        # ----------------------------------------------------
        # UP POSITION
        # ----------------------------------------------------

        elif knee_angle > 160:

            # Count only when we actually came from DOWN
            if self.stage == "down":

                self.reps += 1

                # Good depth
                if self.min_angle < 100:

                    self.good_depth_reps += 1

                # Shallow but acceptable squat
                else:

                    self.shallow_reps += 1

            self.stage = "up"

            self.min_angle = 180

        return self.reps, self.stage

    def get_form_feedback(
        self,
        knee_angle,
        back_angle
    ):

        feedback = []

        # ----------------------------------------------------
        # SQUAT DEPTH
        # ----------------------------------------------------

        if knee_angle < 100:

            feedback.append(
                "Good squat depth"
            )

        elif knee_angle < 120:

            feedback.append(
                "Good squat"
            )

        elif knee_angle < 140:

            feedback.append(
                "Go a little deeper"
            )

        else:

            feedback.append(
                "Squat deeper"
            )

        # ----------------------------------------------------
        # BACK POSTURE
        # ----------------------------------------------------

        if back_angle < 140:

            feedback.append(
                "Keep your back straighter"
            )

        else:

            feedback.append(
                "Good back posture"
            )

        return feedback

    def calculate_score(
        self,
        knee_angle,
        back_angle
    ):

        score = 100

        # ----------------------------------------------------
        # DEPTH SCORE
        # ----------------------------------------------------

        if knee_angle >= 140:

            score -= 40

        elif knee_angle >= 120:

            score -= 20

        # ----------------------------------------------------
        # BACK POSTURE SCORE
        # ----------------------------------------------------

        if back_angle < 140:

            score -= 20

        return max(0, score)

    def get_summary(self):

        if self.reps == 0:

            return {
                "reps": 0,
                "good_depth": 0,
                "shallow": 0,
                "accuracy": 0
            }

        accuracy = (
            self.good_depth_reps
            / self.reps
        ) * 100

        return {
            "reps": self.reps,
            "good_depth": self.good_depth_reps,
            "shallow": self.shallow_reps,
            "accuracy": int(accuracy)
        }