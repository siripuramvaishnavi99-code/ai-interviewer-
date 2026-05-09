AI Interviewer System

An AI-based Interview Preparation and Evaluation System developed using Python, NLP, Computer Vision, and GUI technologies.

This project simulates a technical interview environment where users can:

select interview topics
answer technical questions
get NLP-based answer evaluation
attend coding rounds
monitor concentration using webcam
receive final interview readiness analysis
Features
Technical Interview Simulation
Multiple interview domains
Randomized interview questions
Medium to extremely difficult questions
Timer-based interview environment
NLP-Based Answer Evaluation

Uses:

TF-IDF Vectorization
Cosine Similarity Algorithm

to compare:

user answer
expected technical answer

and generates:

similarity score
technical score
answer feedback
Computer Vision Concentration Monitoring

Uses:

OpenCV
MediaPipe Face Detection

to monitor:

face presence
concentration level
attentiveness during interview
Coding Round

Includes:

coding challenge
binary search implementation test
logic evaluation
Final Performance Report

Generates:

technical score
coding score
concentration score
interview readiness percentage

and saves report locally.

Technologies Used
Technology	Purpose
Python	Main programming language
CustomTkinter	GUI development
OpenCV	Camera monitoring
MediaPipe	Face detection
Scikit-learn	NLP evaluation
TF-IDF	Text vectorization
Cosine Similarity	NLP similarity scoring
Threading	Background camera processing
Algorithms Used
NLP Algorithms
TF-IDF Vectorization

Converts textual answers into numerical vectors.

Cosine Similarity

Measures similarity between:

user answer
expected answer

to calculate technical accuracy.

Computer Vision Algorithms
Face Detection

Detects user presence and calculates concentration level.

Project Structure
AI_Interviewer/
│
├── main.py
├── reports/
│   └── report.txt
└── README.md
Installation Steps
1. Install Anaconda

Download:
https://www.anaconda.com/download

2. Create Environment
conda create -n ai_interviewer python=3.10
3. Activate Environment
conda activate ai_interviewer
4. Install Required Libraries
pip install customtkinter opencv-python mediapipe scikit-learn numpy
Running the Project
Run Application
python main.py
How the System Works
Step 1

Select interview topic:

Python
Machine Learning
DSA
DBMS
Step 2

System generates randomized technical questions.

Step 3

User answers questions within timer limit.

Step 4

NLP algorithm evaluates answers.

Step 5

Webcam monitors concentration level.

Step 6

Coding round evaluates programming logic.

Step 7

Final report generated.

Output

The final report includes:

Technical Score
Coding Score
Concentration Score
Final Readiness Percentage
Performance Level

Saved in:

reports/report.txt
Future Improvements

Possible enhancements:

Voice-based interview system
Emotion detection
Deep learning answer evaluation
Online database integration
Resume analyzer integration
AI-generated dynamic questions
Speech recognition
Applications

This project can be used for:

Interview preparation
Placement training
Technical assessment systems
AI-based learning systems
Academic mini projects
Resume projects
Hackathons
Author

Developed using:

Python
NLP
Computer Vision
Machine Learning Concepts
License

This project is open-source and free for educational purposes
