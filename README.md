🏋️ AI Gym & Fitness Assistant
— AI-Powered Workout, Diet & Habit Coach
An AI-powered fitness assistant that uses your webcam to analyze exercise form in real time, tracks your workout performance and habits, calculates personalized nutrition targets, and answers fitness questions through a conversational AI coach.

The system captures webcam frames, detects body landmarks using MediaPipe Pose, computes joint angles to count repetitions and score form, stores workout results for performance tracking, and uses the Google Gemini LLM to power a "Virtual Gym Buddy" chatbot for fitness, nutrition, and motivation guidance.

The assistant is built as a single Streamlit application and is designed to give real-time, actionable feedback rather than generic fitness advice.

🎯 Project Objective
The main objective of this project is to develop an all-in-one AI fitness assistant that helps users train with correct form, eat according to their goals, stay consistent, and get instant answers to fitness questions — without needing a personal trainer, nutritionist, or separate apps for each task.

Instead of relying on manual rep counting or generic diet charts, the application uses computer vision to observe the user's movement directly and computes personalized nutrition numbers from their own body stats.

Main goals
Capture live webcam video for workout analysis.
Detect body landmarks using MediaPipe Pose.
Calculate joint angles to identify exercise stage and repetitions.
Score workout form and flag posture issues in real time.
Calculate BMI, BMR, and daily calorie needs from user inputs.
Generate a goal-based sample meal plan.
Answer fitness/nutrition/motivation questions using a Gemini-powered chatbot.
Track workout history and visualize performance trends.
Track daily habits, streaks, and weekly consistency.
Avoid crashing or blocking the app when the AI chatbot is unavailable.

✨ Key Features
🏋️ Real-Time Webcam Workout Detection
Users grant camera access through the Streamlit interface and perform exercises directly in front of the browser.

🔍 Landmark-wise Pose Extraction
Video frames are processed page-by-page — frame-by-frame — while preserving:

Shoulder, hip, knee, and ankle coordinates
Left/right side visibility scores
Selected body side (whichever is more clearly visible)
Frames where no person or no leg landmarks are detected are automatically skipped.

✂️ Intelligent Rep & Stage Detection
Knee angles are passed through a dedicated:

SquatDetector state machine

Current configuration:

Visibility threshold: 0.35
Processing frame width: 640px
This helps maintain accurate rep counts even with partial visibility or camera noise.

🧠 Joint Angle Calculations
The project uses:

calculate_angle() geometry function
to convert shoulder/hip/knee/ankle coordinates into knee and back angles used for scoring.

⚡ Live Performance Scoring
Each frame is scored 0–100 based on squat depth and back posture, with good-depth vs. shallow reps tracked separately in real time.

🤖 Gemini-Powered Virtual Gym Buddy
User questions are passed to a Google Gemini LLM to generate the final response.

The current default integration is:

VirtualGymBuddy (google-generativeai)
The client is initialized from a GEMINI_API_KEY environment variable.

📌 Source-Grounded Nutrition Output
The dietician module displays the exact metrics behind every recommendation.

Example:

BMI: 22.4 (Normal)
BMR: 1512 kcal/day
Daily Target: 1814 kcal/day
🛡️ Graceful Degradation
The chatbot is instructed to disable itself cleanly rather than crash the app.

If the Gemini client fails to initialize, the app does not intentionally break the rest of the UI.

🚫 Clear Fallback Messaging
When the Gemini API key is missing or invalid, the chatbot responds:

Gym Buddy is unavailable. Please check your GEMINI_API_KEY in the .env file.
This helps users diagnose configuration issues instead of seeing a silent failure.

🔐 Session-Scoped Data Handling
Workout history, habit records, and chat history are treated as session data, not permanent storage.

The app does not currently:

Persist data across restarts
Write to an external database
Share data between users
Retain chat history after the session ends
🏗️ System Architecture
                    ┌─────────────────────┐
                    │    User Webcam       │
                    │   Video Stream        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Frame Capture      │
                    │  streamlit-webrtc    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Pose Detection      │
                    │  MediaPipe Pose      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Angle Calculation   │
                    │  Knee & Back Angle   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Squat Detector      │
                    │  Rep Count + Score   │
                    └──────────┬───────────┘
                               │
                      Save Workout
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Performance Tracker  │
                    │  + Habit Tracker     │
                    └──────────┬───────────┘
                               │
                       User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Virtual Gym Buddy   │
                    │    Gemini LLM        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Answer + Chat       │
                    │      History         │
                    └─────────────────────┘
🔄 Application Workflow
The application follows these steps:

1. Start Camera
The user grants webcam access and stands sideways to the camera.

2. Detect Pose
pose_detector.py runs MediaPipe Pose on every incoming frame.

Landmarks are preserved for each frame:

shoulder, hip, knee, ankle coordinates
left/right visibility scores
2. Calculate Angles
The more visible body side is selected, and knee/back angles are computed using calculate_angle().

3. Count Reps & Score Form
squat_detector.py converts the knee angle into rep count, movement stage, form feedback, and a 0–100 score.

This prevents the system from over- or under-counting reps during partial movements.

4. Save the Workout
The user clicks "Save Current Workout" to log the session.

5. Update Trackers
performance_tracker.py stores the workout summary, and habit_tracker.py marks the day as completed.

6. Calculate Nutrition
The user enters their weight, height, age, gender, activity level, and goal in the Dietician panel.

diet_calculator.py computes BMI, BMR, and calorie targets; meal_planner.py generates a sample meal plan.

7. Ask a Question
The user enters a message in the Virtual Gym Buddy chat.

8. Generate the Answer
chatbot.py sends the message to the Gemini LLM along with the chatbot's role instructions.

9. Display Progress
The application displays workout history, an accuracy/score trend chart, and the current habit streak.

🛠️ Technologies Used
Technology	Purpose
Python	Main programming language
Streamlit	Web application interface
streamlit-webrtc	Real-time webcam video streaming
OpenCV	Frame resizing, mirroring, and overlay rendering
MediaPipe	Body landmark / pose detection
NumPy	Numerical and angle calculations
python-dotenv	Loading environment variables (API keys)
google-generativeai	Gemini LLM integration for the chatbot
pandas / scikit-learn / Plotly	Reserved for future analytics (not yet wired into the app)
pymongo	Reserved for future persistent storage (not yet wired into the app)

📌 Notes & Limitations

Only squats are currently supported as a tracked exercise.
Workout history, habits, and chat history reset when the app restarts (no database persistence yet).
Pose detection accuracy depends on lighting, camera angle, and joint visibility.
The Smart Gym Assistant (IoT) and Gym Recommender modules are UI placeholders for future work.
