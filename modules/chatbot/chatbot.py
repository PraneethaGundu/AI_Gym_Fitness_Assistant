import os

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


class VirtualGymBuddy:

    def __init__(self):

        if not API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please add it to your .env file."
            )

        self.client = genai.Client(
            api_key=API_KEY
        )

        self.model = "gemini-3.6-flash"

    def ask(self, user_message):

        system_prompt = """
You are Virtual Gym Buddy, an AI fitness assistant.

Your job is to help users with:
- General workout guidance
- Exercise explanations
- Beginner fitness advice
- Workout motivation
- Recovery and rest suggestions
- General nutrition guidance
- Healthy fitness habits

Rules:
1. Give simple and practical answers.
2. Be encouraging and supportive.
3. Do not claim to be a doctor or personal trainer.
4. Do not diagnose medical conditions.
5. For injuries, severe pain, medical conditions, or
   urgent health concerns, recommend consulting a
   qualified healthcare professional.
6. Do not recommend dangerous exercise practices.
7. Do not provide extreme dieting advice.
8. Keep answers suitable for a beginner.
"""

        prompt = f"""
{system_prompt}

User question:
{user_message}

Give a clear and helpful response.
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            return (
                "Sorry, I could not generate a response right now. "
                f"Error: {str(e)}"
            )


if __name__ == "__main__":

    print("=" * 60)
    print("🤖 Virtual Gym Buddy")
    print("=" * 60)

    try:

        buddy = VirtualGymBuddy()

        print("\nType 'exit' to stop.\n")

        while True:

            question = input("You: ")

            if question.lower() == "exit":
                print("Goodbye! Stay consistent with your fitness goals. 💪")
                break

            answer = buddy.ask(question)

            print("\nGym Buddy:")
            print(answer)
            print()

    except Exception as e:

        print("\n❌ Error:")
        print(e)