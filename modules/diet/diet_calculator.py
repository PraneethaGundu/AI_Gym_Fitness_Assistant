def calculate_bmi(weight, height):
    """
    Calculate BMI.

    weight: kilograms
    height: centimeters
    """

    height_m = height / 100

    if height_m <= 0:
        return 0

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


def get_bmi_category(bmi):
    """
    Return BMI category.
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal weight"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def calculate_bmr(weight, height, age, gender):
    """
    Calculate Basal Metabolic Rate using
    the Mifflin-St Jeor equation.
    """

    if gender == "Male":

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    return round(bmr)


def calculate_daily_calories(bmr, activity_level, goal):
    """
    Estimate daily calorie requirement.
    """

    activity_factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }

    calories = bmr * activity_factors.get(
        activity_level,
        1.2
    )

    if goal == "Weight Loss":
        calories -= 300

    elif goal == "Weight Gain":
        calories += 300

    return round(calories)


def get_calorie_message(goal):

    if goal == "Weight Loss":
        return "A moderate calorie deficit can support gradual weight loss."

    elif goal == "Weight Gain":
        return "A moderate calorie surplus can support gradual weight gain."

    else:
        return "Maintain a balanced calorie intake to support your fitness goal."