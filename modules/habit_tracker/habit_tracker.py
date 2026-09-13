
from datetime import date, timedelta


class HabitTracker:

    def __init__(self):

        self.habit_history = {}

    # ========================================================
    # MARK WORKOUT COMPLETE
    # ========================================================

    def mark_workout(self, workout_date=None):

        if workout_date is None:
            workout_date = date.today()

        date_key = workout_date.isoformat()

        self.habit_history[date_key] = True

    # ========================================================
    # REMOVE WORKOUT
    # ========================================================

    def remove_workout(self, workout_date=None):

        if workout_date is None:
            workout_date = date.today()

        date_key = workout_date.isoformat()

        self.habit_history[date_key] = False

    # ========================================================
    # CHECK WORKOUT STATUS
    # ========================================================

    def is_workout_completed(self, workout_date):

        date_key = workout_date.isoformat()

        return self.habit_history.get(
            date_key,
            False
        )

    # ========================================================
    # CURRENT STREAK
    # ========================================================

    def get_current_streak(self):

        today = date.today()

        streak = 0

        current_day = today

        while self.is_workout_completed(current_day):

            streak += 1

            current_day -= timedelta(days=1)

        return streak

    # ========================================================
    # BEST STREAK
    # ========================================================

    def get_best_streak(self):

        if not self.habit_history:
            return 0

        completed_dates = sorted(
            date.fromisoformat(day)
            for day, completed in self.habit_history.items()
            if completed
        )

        if not completed_dates:
            return 0

        best_streak = 1
        current_streak = 1

        for i in range(1, len(completed_dates)):

            difference = (
                completed_dates[i]
                - completed_dates[i - 1]
            ).days

            if difference == 1:

                current_streak += 1

                best_streak = max(
                    best_streak,
                    current_streak
                )

            else:

                current_streak = 1

        return best_streak

    # ========================================================
    # WEEKLY STATISTICS
    # ========================================================

    def get_weekly_stats(self):

        today = date.today()

        start_of_week = (
            today - timedelta(
                days=today.weekday()
            )
        )

        completed = 0

        for i in range(7):

            current_day = (
                start_of_week
                + timedelta(days=i)
            )

            if self.is_workout_completed(current_day):

                completed += 1

        consistency = round(
            (completed / 7) * 100
        )

        return {
            "completed": completed,
            "total": 7,
            "consistency": consistency
        }

    # ========================================================
    # TOTAL WORKOUT DAYS
    # ========================================================

    def get_total_workout_days(self):

        return sum(
            1
            for completed
            in self.habit_history.values()
            if completed
        )
