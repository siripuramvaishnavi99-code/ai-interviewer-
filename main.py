import customtkinter as ctk
from tkinter import messagebox
import cv2
import mediapipe as mp
import threading
import random
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# APPEARANCE
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================================================
# QUESTION DATABASE
# =========================================================

question_bank = {

    "Python": [

        ("What is Python?",
         "Python is a high level interpreted programming language."),

        ("Explain OOP concepts.",
         "OOP concepts include inheritance polymorphism encapsulation and abstraction."),

        ("What is multithreading?",
         "Multithreading allows concurrent execution of threads."),

        ("Explain decorators.",
         "Decorators modify functionality of functions dynamically."),

        ("What is GIL?",
         "GIL is Global Interpreter Lock in Python."),

        ("Difference between list and tuple?",
         "Lists are mutable while tuples are immutable."),

        ("What is exception handling?",
         "Exception handling manages runtime errors using try except."),

        ("Explain generators.",
         "Generators produce values lazily using yield keyword."),

        ("What is lambda function?",
         "Lambda functions are anonymous functions."),

        ("Explain modules in Python.",
         "Modules are reusable python files.")
    ],

    "Machine Learning": [

        ("What is Machine Learning?",
         "Machine learning enables systems to learn from data."),

        ("Explain supervised learning.",
         "Supervised learning uses labeled data."),

        ("What is overfitting?",
         "Overfitting occurs when model memorizes training data."),

        ("Explain linear regression.",
         "Linear regression predicts continuous values."),

        ("What is logistic regression?",
         "Logistic regression is used for binary classification."),

        ("Explain random forest.",
         "Random forest uses multiple decision trees."),

        ("What is gradient descent?",
         "Gradient descent minimizes loss function."),

        ("Explain SVM.",
         "SVM separates classes using hyperplanes."),

        ("What is cross validation?",
         "Cross validation evaluates model performance."),

        ("Explain neural networks.",
         "Neural networks mimic human brain neurons.")
    ],

    "DSA": [

        ("What is binary search?",
         "Binary search divides sorted arrays repeatedly."),

        ("Explain recursion.",
         "Recursion is function calling itself."),

        ("What is dynamic programming?",
         "Dynamic programming stores subproblem solutions."),

        ("Explain BFS.",
         "BFS traverses graph level by level."),

        ("Explain DFS.",
         "DFS explores graph depth wise."),

        ("What is stack?",
         "Stack follows LIFO principle."),

        ("Explain queue.",
         "Queue follows FIFO principle."),

        ("What is heap?",
         "Heap is complete binary tree."),

        ("Explain merge sort.",
         "Merge sort divides and merges arrays."),

        ("What is hashmap?",
         "Hashmap stores key value pairs.")
    ],

    "DBMS": [

        ("What is normalization?",
         "Normalization removes redundancy."),

        ("Explain ACID properties.",
         "ACID properties ensure reliable transactions."),

        ("What is indexing?",
         "Indexing improves query performance."),

        ("Explain joins.",
         "Joins combine rows from tables."),

        ("What is foreign key?",
         "Foreign key links tables."),

        ("Explain transactions.",
         "Transactions are sequences of database operations."),

        ("What is denormalization?",
         "Denormalization improves performance."),

        ("Explain locking.",
         "Locking controls concurrent access."),

        ("What is SQL?",
         "SQL is Structured Query Language."),

        ("Explain views.",
         "Views are virtual tables.")
    ]
}

# =========================================================
# GLOBAL VARIABLES
# =========================================================

questions = []
answers = []

current_question = 0

technical_score = 0
coding_score = 0
concentration_score = 100

face_detected_frames = 0
total_frames = 0

camera_running = False

timer_seconds = 60
timer_job = None

interview_finished = False

# =========================================================
# CAMERA MONITORING
# =========================================================

def monitor_concentration():

    global face_detected_frames
    global total_frames
    global concentration_score
    global camera_running

    mp_face = mp.solutions.face_detection
    detector = mp_face.FaceDetection()

    cap = cv2.VideoCapture(0)

    while camera_running:

        success, frame = cap.read()

        if not success:
            continue

        total_frames += 1

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = detector.process(rgb)

        if results.detections:
            face_detected_frames += 1

        concentration_score = (
            face_detected_frames /
            max(total_frames, 1)
        ) * 100

        cv2.putText(
            frame,
            f"Concentration: {concentration_score:.1f}%",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Concentration Monitor",
            frame
        )

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# =========================================================
# START CAMERA
# =========================================================

def start_camera():

    global camera_running

    camera_running = True

    thread = threading.Thread(
        target=monitor_concentration,
        daemon=True
    )

    thread.start()

# =========================================================
# STOP CAMERA
# =========================================================

def stop_camera():

    global camera_running

    camera_running = False

# =========================================================
# GENERATE QUESTIONS
# =========================================================

def generate_questions():

    global questions
    global answers
    global current_question
    global technical_score
    global interview_finished

    topic = topic_menu.get()

    if topic not in question_bank:

        messagebox.showerror(
            "Error",
            "Select valid topic"
        )
        return

    selected = random.sample(
        question_bank[topic],
        min(10, len(question_bank[topic]))
    )

    questions = [q[0] for q in selected]
    answers = [q[1] for q in selected]

    current_question = 0
    technical_score = 0
    interview_finished = False

    start_btn.configure(state="disabled")

    start_camera()

    show_question()

# =========================================================
# SHOW QUESTION
# =========================================================

def show_question():

    global timer_seconds
    global timer_job
    global interview_finished

    if interview_finished:
        return

    if current_question >= len(questions):

        interview_finished = True

        coding_round()

        return

    if timer_job is not None:
        app.after_cancel(timer_job)

    timer_seconds = 60

    question_label.configure(
        text=f"Q{current_question + 1}: {questions[current_question]}"
    )

    answer_box.delete(
        "1.0",
        "end"
    )

    feedback_box.delete(
        "1.0",
        "end"
    )

    update_timer()

# =========================================================
# TIMER
# =========================================================

def update_timer():

    global timer_seconds
    global timer_job

    timer_label.configure(
        text=f"Time Left: {timer_seconds}s"
    )

    if timer_seconds <= 0:

        skip_question()
        return

    timer_seconds -= 1

    timer_job = app.after(
        1000,
        update_timer
    )

# =========================================================
# NLP EVALUATION
# =========================================================

def evaluate_answer(user_answer, ideal_answer):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [user_answer, ideal_answer]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    score = int(similarity * 10)

    score = max(1, min(score, 10))

    return similarity, score

# =========================================================
# SUBMIT ANSWER
# =========================================================

def submit_answer():

    global technical_score
    global current_question
    global timer_job

    if current_question >= len(questions):
        return

    if timer_job is not None:
        app.after_cancel(timer_job)

    user_answer = answer_box.get(
        "1.0",
        "end"
    ).strip()

    if len(user_answer) < 3:

        messagebox.showwarning(
            "Warning",
            "Please enter valid answer"
        )

        update_timer()
        return

    ideal_answer = answers[current_question]

    similarity, score = evaluate_answer(
        user_answer,
        ideal_answer
    )

    technical_score += score

    feedback = f"""
Similarity Score: {similarity:.2f}

Question Score: {score}/10

Expected Concepts:
{ideal_answer}

Analysis:
"""

    if score >= 8:
        feedback += "Excellent technical understanding."

    elif score >= 6:
        feedback += "Good answer with decent explanation."

    elif score >= 4:
        feedback += "Average answer. Improve concepts."

    else:
        feedback += "Weak answer. Need more preparation."

    feedback_box.delete(
        "1.0",
        "end"
    )

    feedback_box.insert(
        "end",
        feedback
    )

    current_question += 1

    app.after(
        2500,
        show_question
    )

# =========================================================
# SKIP QUESTION
# =========================================================

def skip_question():

    global current_question
    global timer_job

    if timer_job is not None:
        app.after_cancel(timer_job)

    current_question += 1

    show_question()

# =========================================================
# CODING ROUND
# =========================================================

def coding_round():

    global coding_score

    coding_window = ctk.CTkToplevel(app)

    coding_window.geometry("850x650")

    coding_window.title("Coding Round")

    label = ctk.CTkLabel(
        coding_window,
        text="Coding Question:\nImplement Binary Search Logic",
        font=("Arial", 24)
    )

    label.pack(pady=20)

    code_box = ctk.CTkTextbox(
        coding_window,
        width=750,
        height=350
    )

    code_box.pack(pady=20)

    def submit_code():

        global coding_score

        code = code_box.get(
            "1.0",
            "end"
        ).lower()

        score = 0

        if "while" in code:
            score += 3

        if "mid" in code:
            score += 3

        if "left" in code or "low" in code:
            score += 2

        if "right" in code or "high" in code:
            score += 2

        coding_score = score

        coding_window.destroy()

        show_final_result()

    submit_btn = ctk.CTkButton(
        coding_window,
        text="Submit Code",
        command=submit_code,
        width=250,
        height=45
    )

    submit_btn.pack(pady=20)

# =========================================================
# FINAL RESULT
# =========================================================

def show_final_result():

    stop_camera()

    readiness = (
        technical_score * 0.7 +
        concentration_score * 0.2 +
        coding_score * 0.1
    )

    readiness = min(readiness, 100)

    if readiness >= 85:
        level = "Excellent"

    elif readiness >= 70:
        level = "Good"

    elif readiness >= 50:
        level = "Average"

    else:
        level = "Beginner"

    report = f"""
FINAL INTERVIEW REPORT

Technical Score:
{technical_score}

Concentration Score:
{concentration_score:.2f}

Coding Score:
{coding_score}

Final Readiness:
{readiness:.2f}%

Performance Level:
{level}
"""

    os.makedirs(
        "reports",
        exist_ok=True
    )

    with open(
        "reports/report.txt",
        "w"
    ) as file:

        file.write(report)

    messagebox.showinfo(
        "Interview Completed",
        report
    )

    start_btn.configure(state="normal")

# =========================================================
# GUI
# =========================================================

app = ctk.CTk()

app.geometry("1200x950")

app.title("AI Interviewer")

# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(
    app,
    text="AI Interviewer",
    font=("Arial", 40, "bold")
)

title.pack(pady=20)

# =========================================================
# TOPIC MENU
# =========================================================

topic_menu = ctk.CTkComboBox(
    app,
    values=[
        "Python",
        "Machine Learning",
        "DSA",
        "DBMS"
    ],
    width=350,
    height=40
)

topic_menu.pack(pady=10)

# =========================================================
# START BUTTON
# =========================================================

start_btn = ctk.CTkButton(
    app,
    text="Start Interview",
    command=generate_questions,
    width=300,
    height=45,
    font=("Arial", 18)
)

start_btn.pack(pady=20)

# =========================================================
# TIMER LABEL
# =========================================================

timer_label = ctk.CTkLabel(
    app,
    text="Time Left: 60s",
    font=("Arial", 24)
)

timer_label.pack(pady=10)

# =========================================================
# QUESTION LABEL
# =========================================================

question_label = ctk.CTkLabel(
    app,
    text="Questions will appear here",
    wraplength=1000,
    font=("Arial", 24)
)

question_label.pack(pady=20)

# =========================================================
# ANSWER BOX
# =========================================================

answer_box = ctk.CTkTextbox(
    app,
    width=1000,
    height=220,
    font=("Arial", 18)
)

answer_box.pack(pady=20)

# =========================================================
# BUTTONS
# =========================================================

submit_btn = ctk.CTkButton(
    app,
    text="Submit Answer",
    command=submit_answer,
    width=300,
    height=45,
    font=("Arial", 18)
)

submit_btn.pack(pady=10)

skip_btn = ctk.CTkButton(
    app,
    text="Skip Question",
    command=skip_question,
    width=300,
    height=45,
    font=("Arial", 18)
)

skip_btn.pack(pady=10)

# =========================================================
# FEEDBACK BOX
# =========================================================

feedback_box = ctk.CTkTextbox(
    app,
    width=1000,
    height=220,
    font=("Arial", 16)
)

feedback_box.pack(pady=20)

# =========================================================
# RUN
# =========================================================

app.mainloop()