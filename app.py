import cv2
import av
import threading
import streamlit as st
from datetime import datetime, date, timedelta

from streamlit_webrtc import (
    webrtc_streamer,
    WebRtcMode,
    VideoProcessorBase
)


from modules.workout.pose_detector import PoseDetector
from modules.habit_tracker.habit_tracker import HabitTracker
from modules.workout.squat_detector import (
    SquatDetector,
    calculate_angle
)

from modules.diet.diet_calculator import (
    calculate_bmi,
    get_bmi_category,
    calculate_bmr,
    calculate_daily_calories,
    get_calorie_message
)

from modules.diet.meal_planner import generate_meal_plan

from modules.chatbot.chatbot import VirtualGymBuddy

from modules.performance.performance_tracker import (
    PerformanceTracker
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Gym & Fitness Assistant",
    page_icon="🏋️",
    layout="wide"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("🏋️ AI Gym & Fitness Assistant")

st.write(
    "An AI-powered fitness assistant for workout analysis, "
    "nutrition guidance, performance tracking, and fitness support."
)

st.divider()


# ============================================================
# SESSION STATE
# ============================================================

if "performance_tracker" not in st.session_state:

    st.session_state.performance_tracker = (
        PerformanceTracker()
    )

if "habit_tracker" not in st.session_state:

    st.session_state.habit_tracker = (
        HabitTracker()
    )


if "gym_chat_history" not in st.session_state:

    st.session_state.gym_chat_history = []


if "gym_buddy" not in st.session_state:

    try:

        st.session_state.gym_buddy = (
            VirtualGymBuddy()
        )

    except Exception as e:

        st.session_state.gym_buddy = None
        st.session_state.gym_buddy_error = str(e)


# ============================================================
# AI GYM TRAINER
# ============================================================

st.header("🏋️ AI Gym Trainer")

st.write(
    "Use your webcam to analyze squat posture, "
    "count repetitions, and receive form feedback."
)

st.info(
    "📌 Stand sideways to the camera and make sure your "
    "shoulder, hip, knee, and ankle are visible."
)


# ============================================================
# SQUAT VIDEO PROCESSOR
# ============================================================

class SquatVideoProcessor(VideoProcessorBase):

    def __init__(self):

        # ----------------------------------------------------
        # THREAD LOCK
        # ----------------------------------------------------

        self.lock = threading.Lock()

        # ----------------------------------------------------
        # AI COMPONENTS
        # ----------------------------------------------------

        self.pose_detector = PoseDetector()
        self.squat_detector = SquatDetector()

        # ----------------------------------------------------
        # WORKOUT VALUES
        # ----------------------------------------------------

        self.knee_angle = 0
        self.back_angle = 0

        self.reps = 0
        self.stage = "up"
        self.score = 0

        self.good_depth_reps = 0
        self.shallow_reps = 0

        self.feedback = [
            "Stand sideways to the camera"
        ]


    # ========================================================
    # VIDEO FRAME PROCESSING
    # ========================================================

    def recv(self, frame):

        image = frame.to_ndarray(
            format="bgr24"
        )

        # ----------------------------------------------------
        # MIRROR CAMERA
        # ----------------------------------------------------

        image = cv2.flip(
            image,
            1
        )

        # ----------------------------------------------------
        # REDUCE PROCESSING SIZE
        # ----------------------------------------------------

        max_width = 640

        height, width = image.shape[:2]

        if width > max_width:

            scale = max_width / width

            new_width = max_width

            new_height = int(
                height * scale
            )

            image = cv2.resize(
                image,
                (
                    new_width,
                    new_height
                ),
                interpolation=cv2.INTER_AREA
            )

        # ----------------------------------------------------
        # MEDIA PIPE POSE DETECTION
        # ----------------------------------------------------

        display_frame, results = (
            self.pose_detector.detect(image)
        )

        if results.pose_landmarks:

            landmarks = (
                results.pose_landmarks.landmark
            )

            frame_height, frame_width = (
                display_frame.shape[:2]
            )

            # ------------------------------------------------
            # LEFT SIDE LANDMARKS
            # ------------------------------------------------

            left_shoulder = landmarks[11]
            left_hip = landmarks[23]
            left_knee = landmarks[25]
            left_ankle = landmarks[27]

            # ------------------------------------------------
            # RIGHT SIDE LANDMARKS
            # ------------------------------------------------

            right_shoulder = landmarks[12]
            right_hip = landmarks[24]
            right_knee = landmarks[26]
            right_ankle = landmarks[28]

            # ------------------------------------------------
            # VISIBILITY SCORES
            # ------------------------------------------------

            left_score = min(
                left_shoulder.visibility,
                left_hip.visibility,
                left_knee.visibility,
                left_ankle.visibility
            )

            right_score = min(
                right_shoulder.visibility,
                right_hip.visibility,
                right_knee.visibility,
                right_ankle.visibility
            )

            # ------------------------------------------------
            # SELECT MORE VISIBLE SIDE
            # ------------------------------------------------

            if left_score >= 0.35:

                shoulder = left_shoulder
                hip = left_hip
                knee = left_knee
                ankle = left_ankle

            elif right_score >= 0.35:

                shoulder = right_shoulder
                hip = right_hip
                knee = right_knee
                ankle = right_ankle

            else:

                shoulder = None
                hip = None
                knee = None
                ankle = None

            # ------------------------------------------------
            # CALCULATE ANGLES
            # ------------------------------------------------

            if (
                shoulder is not None
                and hip is not None
                and knee is not None
                and ankle is not None
            ):

                shoulder_point = (
                    int(
                        shoulder.x
                        * frame_width
                    ),
                    int(
                        shoulder.y
                        * frame_height
                    )
                )

                hip_point = (
                    int(
                        hip.x
                        * frame_width
                    ),
                    int(
                        hip.y
                        * frame_height
                    )
                )

                knee_point = (
                    int(
                        knee.x
                        * frame_width
                    ),
                    int(
                        knee.y
                        * frame_height
                    )
                )

                ankle_point = (
                    int(
                        ankle.x
                        * frame_width
                    ),
                    int(
                        ankle.y
                        * frame_height
                    )
                )

                # ------------------------------------------------
                # KNEE ANGLE
                # ------------------------------------------------

                knee_angle = calculate_angle(
                    hip_point,
                    knee_point,
                    ankle_point
                )

                # ------------------------------------------------
                # BACK ANGLE
                # ------------------------------------------------

                back_angle = calculate_angle(
                    shoulder_point,
                    hip_point,
                    knee_point
                )

                # ------------------------------------------------
                # WORKOUT PROCESSING
                # ------------------------------------------------

                with self.lock:

                    self.knee_angle = knee_angle

                    self.back_angle = back_angle

                    # ------------------------------------------------
                    # REP COUNTING
                    # ------------------------------------------------

                    self.reps, self.stage = (
                        self.squat_detector.update(
                            self.knee_angle
                        )
                    )

                    # ------------------------------------------------
                    # FORM FEEDBACK
                    # ------------------------------------------------

                    self.feedback = (
                        self.squat_detector.get_form_feedback(
                            self.knee_angle,
                            self.back_angle
                        )
                    )

                    # ------------------------------------------------
                    # PERFORMANCE SCORE
                    # ------------------------------------------------

                    self.score = (
                        self.squat_detector.calculate_score(
                            self.knee_angle,
                            self.back_angle
                        )
                    )

                    # ------------------------------------------------
                    # DEPTH COUNTS
                    # ------------------------------------------------

                    self.good_depth_reps = (
                        self.squat_detector.good_depth_reps
                    )

                    self.shallow_reps = (
                        self.squat_detector.shallow_reps
                    )

            else:

                with self.lock:

                    self.feedback = [
                        "Leg landmarks not fully visible"
                    ]

        else:

            with self.lock:

                self.feedback = [
                    "No person detected"
                ]

        # ====================================================
        # VIDEO OVERLAY
        # ====================================================

        with self.lock:

            display_reps = self.reps
            display_knee = self.knee_angle
            display_back = self.back_angle
            display_stage = self.stage
            display_score = self.score
            display_feedback = list(self.feedback)

        # ----------------------------------------------------
        # REPS
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            f"Reps: {display_reps}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2
        )

        # ----------------------------------------------------
        # KNEE
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            f"Knee: {int(display_knee)} deg",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (255, 255, 255),
            2
        )

        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            f"Back: {int(display_back)} deg",
            (20, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (255, 255, 255),
            2
        )

        # ----------------------------------------------------
        # STAGE
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            f"Stage: {display_stage}",
            (20, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (255, 255, 255),
            2
        )

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            f"Score: {display_score}/100",
            (20, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            (0, 255, 255),
            2
        )

        # ----------------------------------------------------
        # FEEDBACK
        # ----------------------------------------------------

        y_position = 195

        for message in display_feedback:

            cv2.putText(
                display_frame,
                message,
                (20, y_position),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 255),
                2
            )

            y_position += 30

        # ----------------------------------------------------
        # RETURN FRAME
        # ----------------------------------------------------

        return av.VideoFrame.from_ndarray(
            display_frame,
            format="bgr24"
        )


    # ========================================================
    # GET CURRENT WORKOUT STATISTICS
    # ========================================================

    def get_workout_stats(self):

        with self.lock:

            return {
                "reps": self.reps,
                "good_depth": self.good_depth_reps,
                "shallow": self.shallow_reps,
                "score": self.score,
                "stage": self.stage,
                "knee_angle": self.knee_angle,
                "back_angle": self.back_angle
            }


    # ========================================================
    # RESET WORKOUT
    # ========================================================

    def reset_workout(self):

        with self.lock:

            self.squat_detector = SquatDetector()

            self.knee_angle = 0
            self.back_angle = 0

            self.reps = 0
            self.stage = "up"
            self.score = 0

            self.good_depth_reps = 0
            self.shallow_reps = 0

            self.feedback = [
                "Stand sideways to the camera"
            ]


    # ========================================================
    # CLEANUP
    # ========================================================

    def __del__(self):

        try:

            self.pose_detector.close()

        except Exception:

            pass


# ============================================================
# WEBRTC CAMERA
# ============================================================

ctx = webrtc_streamer(
    key="squat-trainer-live",

    mode=WebRtcMode.SENDRECV,

    video_processor_factory=SquatVideoProcessor,

    media_stream_constraints={
        "video": {
            "width": {
                "ideal": 640
            },
            "height": {
                "ideal": 480
            },
            "frameRate": {
                "ideal": 24
            }
        },
        "audio": False
    },

    async_processing=True
)

# ============================================================
# CURRENT WORKOUT
# ============================================================

st.subheader("📊 Current Workout")

st.write(
    "Your workout statistics are automatically "
    "collected from the AI Gym Trainer."
)


# ------------------------------------------------------------
# DEFAULT VALUES
# ------------------------------------------------------------

current_stats = {
    "reps": 0,
    "good_depth": 0,
    "shallow": 0,
    "score": 0,
    "stage": "up",
    "knee_angle": 0,
    "back_angle": 0
}


# ------------------------------------------------------------
# GET VALUES DIRECTLY FROM VIDEO PROCESSOR
# ------------------------------------------------------------

if ctx.video_processor is not None:

    current_stats = (
        ctx.video_processor.get_workout_stats()
    )


# ============================================================
# LIVE WORKOUT METRICS
# ============================================================

current_col1, current_col2, current_col3, current_col4 = (
    st.columns(4)
)


with current_col1:

    st.metric(
        "Reps",
        current_stats["reps"]
    )


with current_col2:

    st.metric(
        "Good Depth",
        current_stats["good_depth"]
    )


with current_col3:

    st.metric(
        "Shallow",
        current_stats["shallow"]
    )


with current_col4:

    st.metric(
        "Current Score",
        f'{current_stats["score"]}/100'
    )


# ============================================================
# LIVE DETAILS
# ============================================================

detail_col1, detail_col2, detail_col3 = st.columns(3)


with detail_col1:

    st.write(
        f"**Stage:** {current_stats['stage']}"
    )


with detail_col2:

    st.write(
        f"**Knee Angle:** "
        f"{int(current_stats['knee_angle'])}°"
    )


with detail_col3:

    st.write(
        f"**Back Angle:** "
        f"{int(current_stats['back_angle'])}°"
    )


# ============================================================
# SAVE CURRENT WORKOUT
# ============================================================

st.subheader("💾 Save Current Workout")


current_reps = current_stats["reps"]

current_good = current_stats["good_depth"]

current_shallow = current_stats["shallow"]

current_score = current_stats["score"]


# ------------------------------------------------------------
# WORKOUT STATUS
# ------------------------------------------------------------

if current_reps > 0:

    st.success(
        f"Workout detected: {current_reps} completed rep(s)."
    )

else:

    st.info(
        "Complete some squats using the camera first."
    )


# ------------------------------------------------------------
# SAVE BUTTON
# ------------------------------------------------------------

if st.button(
    "💾 Save Current Workout",
    use_container_width=True
):

    if current_reps == 0:

        st.warning(
            "Please complete at least one squat "
            "before saving the workout."
        )

    else:

        tracker = (
            st.session_state.performance_tracker
        )

        # ------------------------------------------------
        # SAVE AUTOMATICALLY DETECTED VALUES
        # ------------------------------------------------

        record = tracker.create_workout_record(
            exercise="Squat",
            total_reps=current_reps,
            good_reps=current_good,
            shallow_reps=current_shallow,
            average_score=current_score
        )

        # ------------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------------

        st.success(
            "✅ Current workout saved successfully!"
        )

        st.write(
            f"**Reps:** {record['total_reps']}"
        )

        st.write(
            f"**Good Depth:** {record['good_reps']}"
        )

        st.write(
            f"**Shallow:** {record['shallow_reps']}"
        )

        st.write(
            f"**Workout Accuracy:** "
            f"{record['accuracy']}%"
        )

        st.write(
            f"**Workout Score:** "
            f"{record['average_score']}/100"
        )

        # ------------------------------------------------
        # RESET FOR NEXT WORKOUT
        # ------------------------------------------------

        if ctx.video_processor is not None:

            ctx.video_processor.reset_workout()

        st.rerun()


st.divider()


# ============================================================
# AI DIETICIAN
# ============================================================

st.header("🥗 AI Dietician & Calorie Coach")

st.write(
    "Calculate BMI, BMR, daily calorie requirements, "
    "and generate a simple meal plan."
)


diet_col1, diet_col2 = st.columns(2)


with diet_col1:

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        value=60.0,
        step=1.0
    )

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=250.0,
        value=165.0,
        step=1.0
    )

    age = st.number_input(
        "Age",
        min_value=13,
        max_value=100,
        value=20,
        step=1
    )


with diet_col2:

    gender = st.selectbox(
        "Gender",
        [
            "Female",
            "Male"
        ]
    )

    activity_level = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active"
        ]
    )

    goal = st.selectbox(
        "Fitness Goal",
        [
            "Weight Loss",
            "Maintenance",
            "Weight Gain"
        ]
    )


diet_type = st.selectbox(
    "Diet Type",
    [
        "Vegetarian",
        "Non-Vegetarian"
    ]
)


# ============================================================
# CALCULATE NUTRITION
# ============================================================

if st.button(
    "🥗 Calculate Fitness Nutrition",
    use_container_width=True
):

    bmi = calculate_bmi(
        weight,
        height
    )

    bmi_category = get_bmi_category(
        bmi
    )

    bmr = calculate_bmr(
        weight,
        height,
        age,
        gender
    )

    daily_calories = calculate_daily_calories(
        bmr,
        activity_level,
        goal
    )

    st.subheader(
        "📊 Your Nutrition Results"
    )


    result_col1, result_col2, result_col3 = (
        st.columns(3)
    )


    with result_col1:

        st.metric(
            "BMI",
            bmi
        )

        st.write(
            f"Category: **{bmi_category}**"
        )


    with result_col2:

        st.metric(
            "BMR",
            f"{bmr} kcal/day"
        )


    with result_col3:

        st.metric(
            "Daily Target",
            f"{daily_calories} kcal/day"
        )


    st.info(
        get_calorie_message(goal)
    )


    # ========================================================
    # MEAL PLAN
    # ========================================================

    st.subheader(
        "🍽️ Suggested Meal Plan"
    )

    meal_plan = generate_meal_plan(
        daily_calories,
        goal,
        diet_type
    )


    meal_columns = st.columns(4)


    meal_names = [
        "Breakfast",
        "Lunch",
        "Snack",
        "Dinner"
    ]


    for column, meal_name in zip(
        meal_columns,
        meal_names
    ):

        with column:

            st.markdown(
                f"### {meal_name}"
            )

            st.write(
                meal_plan[meal_name]["meal"]
            )

            st.caption(
                f'{meal_plan[meal_name]["calories"]} kcal'
            )


st.divider()


# ============================================================
# VIRTUAL GYM BUDDY
# ============================================================

st.header("🤖 Virtual Gym Buddy")

st.write(
    "Ask the AI Gym Buddy about workouts, nutrition, "
    "motivation, recovery, and general fitness guidance."
)


# ------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------------------------------------

for message in st.session_state.gym_chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ------------------------------------------------------------
# CHAT INPUT
# ------------------------------------------------------------

user_message = st.chat_input(
    "Ask your Virtual Gym Buddy..."
)


if user_message:

    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    st.session_state.gym_chat_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    if st.session_state.gym_buddy is not None:

        with st.chat_message("assistant"):

            with st.spinner(
                "Gym Buddy is thinking..."
            ):

                response = (
                    st.session_state.gym_buddy.ask(
                        user_message
                    )
                )


            st.markdown(
                response
            )


        st.session_state.gym_chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )


    else:

        st.error(
            "Gym Buddy is unavailable. "
            "Please check your GEMINI_API_KEY "
            "in the .env file."
        )


# ------------------------------------------------------------
# CLEAR CHAT
# ------------------------------------------------------------

if st.session_state.gym_chat_history:

    if st.button(
        "🗑️ Clear Gym Buddy Chat"
    ):

        st.session_state.gym_chat_history = []

        st.rerun()


st.divider()


# ============================================================
# PERFORMANCE TRACKING
# ============================================================

st.header("📊 Performance Tracking")

st.write(
    "Track your saved workout history, accuracy, "
    "repetitions, and average performance."
)


tracker = (
    st.session_state.performance_tracker
)


summary = tracker.get_summary()


# ============================================================
# PERFORMANCE SUMMARY
# ============================================================

performance_col1, performance_col2, performance_col3, performance_col4 = (
    st.columns(4)
)


with performance_col1:

    st.metric(
        "Workouts",
        summary["workouts"]
    )


with performance_col2:

    st.metric(
        "Total Reps",
        summary["total_reps"]
    )


with performance_col3:

    st.metric(
        "Avg Accuracy",
        f'{summary["average_accuracy"]}%'
    )


with performance_col4:

    st.metric(
        "Avg Score",
        f'{summary["average_score"]}/100'
    )


# ============================================================
# WORKOUT HISTORY
# ============================================================

if tracker.workout_history:

    st.subheader(
        "📋 Workout History"
    )


    history_data = (
        tracker.workout_history
    )


    st.dataframe(
        history_data,
        use_container_width=True
    )


    # ========================================================
    # PERFORMANCE PROGRESS
    # ========================================================

    st.subheader(
        "📈 Performance Progress"
    )


    chart_data = []


    for index, record in enumerate(
        history_data,
        start=1
    ):

        chart_data.append(
            {
                "Workout": index,
                "Accuracy": record["accuracy"],
                "Score": record["average_score"]
            }
        )


    st.line_chart(
        chart_data,
        x="Workout",
        y=[
            "Accuracy",
            "Score"
        ]
    )


else:

    st.info(
        "Complete and save a workout to see "
        "your performance history and progress chart."
    )


st.divider()

# ============================================================
# FITNESS HABIT TRACKER
# ============================================================

st.header("🔥 Fitness Habit Tracker")

st.write(
    "Build consistency, maintain your workout streak, "
    "and track your fitness habits."
)


habit_tracker = (
    st.session_state.habit_tracker
)


# ============================================================
# WEEKLY STATISTICS
# ============================================================

weekly_stats = (
    habit_tracker.get_weekly_stats()
)

current_streak = (
    habit_tracker.get_current_streak()
)

best_streak = (
    habit_tracker.get_best_streak()
)

total_workout_days = (
    habit_tracker.get_total_workout_days()
)


habit_col1, habit_col2, habit_col3, habit_col4 = (
    st.columns(4)
)


with habit_col1:

    st.metric(
        "🔥 Current Streak",
        f"{current_streak} days"
    )


with habit_col2:

    st.metric(
        "🏆 Best Streak",
        f"{best_streak} days"
    )


with habit_col3:

    st.metric(
        "💪 This Week",
        f'{weekly_stats["completed"]}/7'
    )


with habit_col4:

    st.metric(
        "📊 Consistency",
        f'{weekly_stats["consistency"]}%'
    )


# ============================================================
# WEEKLY HABIT CALENDAR
# ============================================================

st.subheader("📅 This Week")


today = date.today()

start_of_week = (
    today - timedelta(
        days=today.weekday()
    )
)

week_columns = st.columns(7)

day_names = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]


for i, column in enumerate(week_columns):

    current_day = (
        start_of_week
        + timedelta(days=i)
    )

    completed = (
        habit_tracker.is_workout_completed(
            current_day
        )
    )

    with column:

        st.markdown(
            f"**{day_names[i]}**"
        )

        st.caption(
            current_day.strftime("%d %b")
        )

        if completed:

            st.success(
                "✅ Done"
            )

        else:

            st.info(
                "⬜ Rest"
            )


# ============================================================
# MARK TODAY'S WORKOUT
# ============================================================

st.subheader("🏋️ Today's Habit")


today_completed = (
    habit_tracker.is_workout_completed(
        today
    )
)


if today_completed:

    st.success(
        "🎉 Today's workout is completed!"
    )

    if st.button(
        "↩️ Undo Today's Workout",
        use_container_width=True
    ):

        habit_tracker.remove_workout(today)

        st.rerun()

else:

    st.info(
        "You haven't marked today's workout yet."
    )

    if st.button(
        "✅ Mark Today's Workout Complete",
        use_container_width=True
    ):

        habit_tracker.mark_workout(today)

        st.success(
            "🔥 Great job! Your workout has been added "
            "to today's habit tracker."
        )

        st.rerun()


# ============================================================
# MOTIVATION
# ============================================================

st.subheader("💬 Daily Motivation")


if current_streak == 0:

    motivation = (
        "💪 Start today! Your first workout is "
        "the beginning of your streak."
    )

elif current_streak < 3:

    motivation = (
        "🔥 Great start! Keep going and build "
        "your consistency."
    )

elif current_streak < 7:

    motivation = (
        "🚀 You're building a strong habit! "
        "Don't break the streak."
    )

else:

    motivation = (
        "🏆 Amazing consistency! You're maintaining "
        "a powerful fitness habit."
    )


st.info(motivation)


# ============================================================
# TOTAL WORKOUT DAYS
# ============================================================

st.caption(
    f"🏋️ Total workout days tracked: "
    f"{total_workout_days}"
)


# ============================================================
# GYM RECOMMENDER & PLANNER
# ============================================================

st.header("📍 Gym Recommender & Planner")

st.info(
    "Workout planning, gym recommendations, "
    "and fitness challenge suggestions will be "
    "added as an upcoming module."
)


# ============================================================
# SMART GYM ASSISTANT
# ============================================================

st.header("📡 Smart Gym Assistant")

st.info(
    "IoT equipment integration using MQTT/Node-RED "
    "will be added as an advanced module."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏋️ AI Gym & Fitness Assistant | "
    "Student AI/ML Project"
)