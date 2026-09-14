from datetime import date, timedelta


class HabitTracker:
    """
    Fitness Habit Tracker.

    A workout day is considered completed when the user
    completes and saves a workout.
    """

    def __init__(self):
        self.completed_days = set()

    # ============================================================
    # MARK WORKOUT
    # ============================================================

    def mark_workout(self, workout_date=None):

        if workout_date is None:
            workout_date = date.today()

        if isinstance(workout_date, str):
            workout_date = date.fromisoformat(workout_date)

        self.completed_days.add(workout_date)

        return True

    # ============================================================
    # REMOVE WORKOUT
    # ============================================================

    def remove_workout(self, workout_date=None):

        if workout_date is None:
            workout_date = date.today()

        if isinstance(workout_date, str):
            workout_date = date.fromisoformat(workout_date)

        self.completed_days.discard(workout_date)

        return True

    # ============================================================
    # CHECK WORKOUT
    # ============================================================

    def is_workout_completed(self, workout_date=None):

        if workout_date is None:
            workout_date = date.today()

        if isinstance(workout_date, str):
            workout_date = date.fromisoformat(workout_date)

        return workout_date in self.completed_days

    # ============================================================
    # CURRENT STREAK
    # ============================================================

    def get_current_streak(self):

        if not self.completed_days:
            return 0

        today = date.today()

        # If today is completed, streak starts today.
        if today in self.completed_days:
            current_day = today

        # Otherwise check whether yesterday was completed.
        else:
            current_day = today - timedelta(days=1)

            if current_day not in self.completed_days:
                return 0

        streak = 0

        while current_day in self.completed_days:

            streak += 1

            current_day -= timedelta(days=1)

        return streak

    # ============================================================
    # BEST STREAK
    # ============================================================

    def get_best_streak(self):

        if not self.completed_days:
            return 0

        sorted_days = sorted(self.completed_days)

        best_streak = 1
        current_streak = 1

        for i in range(1, len(sorted_days)):

            difference = (
                sorted_days[i] - sorted_days[i - 1]
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

    # ============================================================
    # TOTAL WORKOUT DAYS
    # ============================================================

    def get_total_workout_days(self):

        return len(self.completed_days)

    # ============================================================
    # WEEKLY STATISTICS
    # ============================================================

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
                start_of_week + timedelta(days=i)
            )

            if current_day in self.completed_days:

                completed += 1

        consistency = (
            completed / 7
        ) * 100

        return {
            "completed": completed,
            "consistency": round(consistency, 2)
        }

    # ============================================================
    # MONTHLY STATISTICS
    # ============================================================

    def get_monthly_consistency(self):

        today = date.today()

        completed = 0

        for i in range(30):

            current_day = (
                today - timedelta(days=i)
            )

            if current_day in self.completed_days:

                completed += 1

        return round(
            (completed / 30) * 100,
            2
        )

    # ============================================================
    # GET COMPLETED DATES
    # ============================================================

    def get_completed_dates(self):

        return sorted(self.completed_days)

    # ============================================================
    # SUMMARY
    # ============================================================

    def get_summary(self):

        weekly_stats = self.get_weekly_stats()

        return {
            "current_streak": self.get_current_streak(),
            "best_streak": self.get_best_streak(),
            "total_workout_days": self.get_total_workout_days(),
            "weekly_completed": weekly_stats["completed"],
            "weekly_consistency": weekly_stats["consistency"],
            "monthly_consistency": self.get_monthly_consistency()
        }