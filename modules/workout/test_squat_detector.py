from squat_detector import calculate_angle


def main():
    # Example points representing a bent knee
    hip = (100, 100)
    knee = (100, 200)
    ankle = (150, 250)

    angle = calculate_angle(hip, knee, ankle)

    print(f"Knee angle: {angle:.2f} degrees")


if __name__ == "__main__":
    main()