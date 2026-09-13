def generate_meal_plan(calories, goal, diet_type):
    """
    Generate a simple personalized meal plan.
    """

    breakfast_calories = int(calories * 0.25)
    lunch_calories = int(calories * 0.30)
    snack_calories = int(calories * 0.10)
    dinner_calories = int(calories * 0.35)

    if diet_type == "Vegetarian":

        breakfast = [
            "Oats with milk and banana",
            "Vegetable upma",
            "Idli with sambar"
        ]

        lunch = [
            "Rice with dal and vegetables",
            "Roti with paneer curry and salad",
            "Vegetable pulao with curd"
        ]

        snack = [
            "Fruit with yogurt",
            "Roasted peanuts",
            "Sprouts salad"
        ]

        dinner = [
            "Roti with mixed vegetables",
            "Paneer with vegetables and roti",
            "Dal with rice and salad"
        ]

    else:

        breakfast = [
            "Oats with milk and boiled eggs",
            "Egg sandwich with fruit",
            "Vegetable omelette with toast"
        ]

        lunch = [
            "Rice with chicken and vegetables",
            "Chicken curry with roti and salad",
            "Rice with fish and vegetables"
        ]

        snack = [
            "Fruit with yogurt",
            "Boiled eggs",
            "Roasted peanuts"
        ]

        dinner = [
            "Chicken with vegetables and roti",
            "Grilled fish with salad",
            "Egg curry with roti"
        ]

    # Select first option for a consistent basic plan
    meal_plan = {
        "Breakfast": {
            "meal": breakfast[0],
            "calories": breakfast_calories
        },
        "Lunch": {
            "meal": lunch[0],
            "calories": lunch_calories
        },
        "Snack": {
            "meal": snack[0],
            "calories": snack_calories
        },
        "Dinner": {
            "meal": dinner[0],
            "calories": dinner_calories
        }
    }

    return meal_plan