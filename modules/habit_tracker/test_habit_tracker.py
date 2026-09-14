from datetime import date, timedelta

from habit_tracker import HabitTracker


def main():

    tracker = HabitTracker()

    today = date.today()

    # Simulate 3 consecutive workout days
    tracker.mark_workout(
        today - timedelta(days=2)
    )

    tracker.mark_workout(
        today - timedelta(days=1)
    )

    tracker.mark_workout(today)

    print("=" * 60)
    print("🏋️ FITNESS HABIT TRACKER TEST")
    print("=" * 60)

    print("\nCompleted Dates:")

    for completed_date in tracker.get_completed_dates():

        print(completed_date)

    print("\nHabit Statistics:")

    weekly_stats = tracker.get_weekly_stats()

    print(
        f"Current Streak: "
        f"{tracker.get_current_streak()} days"
    )

    print(
        f"Best Streak: "
        f"{tracker.get_best_streak()} days"
    )

    print(
        f"Total Workout Days: "
        f"{tracker.get_total_workout_days()}"
    )

    print(
        f"This Week: "
        f"{weekly_stats['completed']}/7"
    )

    print(
        f"Weekly Consistency: "
        f"{weekly_stats['consistency']}%"
    )

    print(
        f"Monthly Consistency: "
        f"{tracker.get_monthly_consistency()}%"
    )

    print("\nToday's Status:")

    if tracker.is_workout_completed(today):

        print("✅ Today's workout is completed.")

    else:

        print("❌ Today's workout is not completed.")


if __name__ == "__main__":
    main()