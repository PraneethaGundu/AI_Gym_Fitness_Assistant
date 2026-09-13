from diet_calculator import (
    calculate_bmi,
    get_bmi_category,
    calculate_bmr,
    calculate_daily_calories
)


def main():

    weight = 60
    height = 165
    age = 20
    gender = "Female"

    activity = "Moderately Active"
    goal = "Weight Loss"

    bmi = calculate_bmi(weight, height)

    category = get_bmi_category(bmi)

    bmr = calculate_bmr(
        weight,
        height,
        age,
        gender
    )

    calories = calculate_daily_calories(
        bmr,
        activity,
        goal
    )

    print("=" * 50)
    print("AI DIETICIAN CALCULATOR")
    print("=" * 50)

    print(f"Weight       : {weight} kg")
    print(f"Height       : {height} cm")
    print(f"Age          : {age}")
    print(f"Gender       : {gender}")
    print(f"Activity     : {activity}")
    print(f"Goal         : {goal}")

    print("-" * 50)

    print(f"BMI          : {bmi}")
    print(f"BMI Category : {category}")
    print(f"BMR          : {bmr} calories/day")
    print(f"Daily Target : {calories} calories/day")

    print("=" * 50)


if __name__ == "__main__":
    main()