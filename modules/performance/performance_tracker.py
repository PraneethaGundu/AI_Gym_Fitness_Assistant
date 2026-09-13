from datetime import datetime


class PerformanceTracker:

    def __init__(self):
        self.workout_history = []

    def calculate_accuracy(self, good_reps, total_reps):
        if total_reps == 0:
            return 0

        return round(
            (good_reps / total_reps) * 100,
            2
        )

    def create_workout_record(
        self,
        exercise,
        total_reps,
        good_reps,
        shallow_reps,
        average_score
    ):

        accuracy = self.calculate_accuracy(
            good_reps,
            total_reps
        )

        record = {
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "exercise": exercise,
            "total_reps": total_reps,
            "good_reps": good_reps,
            "shallow_reps": shallow_reps,
            "accuracy": accuracy,
            "average_score": average_score
        }

        self.workout_history.append(record)

        return record

    def get_summary(self):

        if not self.workout_history:
            return {
                "workouts": 0,
                "total_reps": 0,
                "average_accuracy": 0,
                "average_score": 0
            }

        total_reps = sum(
            record["total_reps"]
            for record in self.workout_history
        )

        average_accuracy = sum(
            record["accuracy"]
            for record in self.workout_history
        ) / len(self.workout_history)

        average_score = sum(
            record["average_score"]
            for record in self.workout_history
        ) / len(self.workout_history)

        return {
            "workouts": len(self.workout_history),
            "total_reps": total_reps,
            "average_accuracy": round(
                average_accuracy,
                2
            ),
            "average_score": round(
                average_score,
                2
            )
        }