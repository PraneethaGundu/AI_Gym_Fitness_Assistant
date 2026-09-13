from performance_tracker import PerformanceTracker


def main():

    tracker = PerformanceTracker()

    record1 = tracker.create_workout_record(
        exercise="Squat",
        total_reps=10,
        good_reps=8,
        shallow_reps=2,
        average_score=85
    )

    record2 = tracker.create_workout_record(
        exercise="Squat",
        total_reps=12,
        good_reps=10,
        shallow_reps=2,
        average_score=90
    )

    print("=" * 50)
    print("📊 PERFORMANCE TRACKER TEST")
    print("=" * 50)

    print("\nWorkout 1:")
    print(record1)

    print("\nWorkout 2:")
    print(record2)

    summary = tracker.get_summary()

    print("\nOverall Summary:")
    print(f"Workouts: {summary['workouts']}")
    print(f"Total Reps: {summary['total_reps']}")
    print(
        f"Average Accuracy: "
        f"{summary['average_accuracy']}%"
    )
    print(
        f"Average Score: "
        f"{summary['average_score']}/100"
    )


if __name__ == "__main__":
    main()