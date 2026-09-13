from meal_planner import generate_meal_plan


def main():

    calories = 1824
    goal = "Weight Loss"
    diet_type = "Vegetarian"

    meal_plan = generate_meal_plan(
        calories,
        goal,
        diet_type
    )

    print("=" * 60)
    print("🥗 AI DIETICIAN - MEAL PLAN")
    print("=" * 60)

    print(f"Daily Calories : {calories}")
    print(f"Goal           : {goal}")
    print(f"Diet Type      : {diet_type}")

    print("-" * 60)

    for meal, details in meal_plan.items():

        print(
            f"{meal:<10} : "
            f"{details['meal']} "
            f"({details['calories']} kcal)"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()