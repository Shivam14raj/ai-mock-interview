# 🤖 AI-Powered Mock Interview

> An AI-powered technical mock interview platform that analyzes a candidate's resume, generates personalized interview questions, evaluates spoken answers using Google Gemini, performs real-time facial-expression analysis, and provides a detailed final performance report.

---

## 📌 About The Project

The **AI-Powered Mock Interview** is an interactive interview-preparation application built with **Python and Streamlit**.

The application simulates a technical interview by combining **Generative AI, Computer Vision, Speech-to-Text, and Deep Learning**.

Instead of asking a fixed set of generic questions, the system analyzes the candidate's uploaded resume and generates questions based on their actual:

- Technical skills
- Projects
- Internships
- Technologies
- Work experience
- Problem-solving experience

The interview consists of **5 dynamically generated questions**. After every answer, the AI evaluates the response and uses the interview history to generate the next question.

At the end of the interview, the system generates an AI-powered performance report containing scores, strengths, weaknesses, improvement suggestions, and question-by-question feedback.

---

# ✨ Key Features

## 📄 1. Resume-Based Interview

The candidate uploads their resume in **PDF format**.

The resume is uploaded to the Gemini API and provided to the AI interviewer as context.

The AI analyzes the resume and generates the first technical question specifically around the candidate's background.

The system avoids generic questions such as:

> "Tell me about yourself."

Instead, questions focus on the candidate's actual projects, skills, internships, technologies, and experience.

---

## 🤖 2. AI Technical Interviewer

**Google Gemini** acts as the technical interviewer.

The AI is responsible for:

- Resume analysis
- Technical question generation
- Answer evaluation
- Adaptive follow-up questions
- Difficulty adjustment
- Final interview analysis
- Performance report generation

The interviewer is designed to behave dynamically rather than following a hardcoded question list.

---

## 🔄 3. Adaptive Interview Questions

One of the main features of the project is adaptive question generation.

After each answer, the system sends the previous interview history to Gemini.

The AI considers:

- Previous questions
- Candidate answers
- Previous evaluations
- Resume information
- Candidate's demonstrated understanding

The next question can then be adapted accordingly.

### Example

```text
Candidate gives a weak answer
        ↓
AI identifies the weak area
        ↓
Next question goes deeper into that concept
```

If the candidate demonstrates strong understanding:

```text
Strong answer
     ↓
AI recognizes strong understanding
     ↓
Difficulty can be increased
     ↓
More advanced question
```

The system also instructs Gemini not to repeat previous questions.

---

# 🎤 4. Speech-to-Text

Candidates can answer interview questions using their microphone.

The application uses:

**Streamlit Mic Recorder**

to capture the candidate's spoken answer and convert it into text.

The generated transcript is displayed in the interface before submission.

### Flow

```text
Microphone
     ↓
Candidate speaks
     ↓
Speech-to-Text
     ↓
Transcript
     ↓
Candidate reviews answer
     ↓
Submit Answer
```

---

# 😊 5. Real-Time Facial Emotion Detection

The application includes a webcam-based facial-expression recognition feature.

The candidate's webcam is streamed using:

**Streamlit-WebRTC**

Frames are processed locally using **OpenCV**.

A pretrained deep-learning emotion model is then used to classify the detected facial expression.

### Supported emotions

```text
Angry
Disgust
Fear
Happy
Neutral
Sad
Surprise
```

The detected emotion and prediction confidence are displayed directly on the webcam feed.

> **Important:** Facial-expression recognition is an experimental computer-vision feature and should not be interpreted as a reliable measurement of a candidate's psychological state, confidence, personality, or hiring suitability.

---

# 🧠 AI & Machine Learning Components

## 1. Google Gemini

Gemini is the primary Generative AI component.

It is used for:

```text
Resume Analysis
      ↓
Question Generation
      ↓
Answer Evaluation
      ↓
Adaptive Question Generation
      ↓
Final Performance Report
```

The application uses the Google GenAI Python SDK.

---

## 2. Facial Emotion Recognition Model

The project uses a pretrained Keras model hosted on Hugging Face.

### Model Repository

```text
lokeshkumar79/facial-emotion-recognition
```

### Model File

```text
finalfacialemotionmodel.keras
```

The model expects a grayscale facial image resized to:

```text
48 × 48 × 1
```

Pixel values are normalized to the range:

```text
0 – 1
```

before prediction.

---

# 👁️ Computer Vision Pipeline

The webcam processing pipeline works as follows:

```text
             Webcam Frame
                   │
                   ▼
          Convert to BGR Image
                   │
                   ▼
           Convert to Grayscale
                   │
                   ▼
          Haar Cascade Detection
                   │
                   ▼
             Detect Face
                   │
                   ▼
             Crop Face
                   │
                   ▼
           Resize to 48 × 48
                   │
                   ▼
        Normalize Pixel Values
                   │
                   ▼
          Reshape to 48×48×1
                   │
                   ▼
        Emotion Recognition Model
                   │
                   ▼
       Predicted Emotion + Confidence
```

OpenCV's Haar Cascade is used for face detection before the facial image is passed to the emotion-recognition model.

---

# 🧪 Answer Evaluation

Every submitted answer is evaluated by Gemini.

The evaluation considers:

1. Technical correctness
2. Relevance
3. Clarity
4. Depth of understanding
5. Completeness

The AI generates:

- Score out of 10
- Technical correctness
- Relevance
- Clarity
- Strengths
- Weaknesses
- Specific improvement suggestions

The evaluation is instructed to remain honest and critical instead of giving a high score simply because an answer sounds confident.

---

# 📊 Final Performance Report

After all 5 questions are completed, Gemini analyzes the complete interview history.

The final report contains:

### Overall Score

A score between:

```text
0 – 100
```

### Performance Metrics

Each individual metric is scored from:

```text
0 – 10
```

The report includes:

- Technical Knowledge
- Communication
- Problem Solving
- Answer Relevance

### Additional Feedback

The report also contains:

- Strengths
- Weaknesses
- Improvement Plan
- Overall Interviewer Feedback
- Question-by-question analysis

---

# 📈 Final Report Structure

The AI generates a structured JSON response containing:

```json
{
  "overall_score": 0,
  "technical_knowledge": 0,
  "communication": 0,
  "problem_solving": 0,
  "answer_relevance": 0,
  "strengths": [
    "strength 1",
    "strength 2",
    "strength 3"
  ],
  "weaknesses": [
    "weakness 1",
    "weakness 2",
    "weakness 3"
  ],
  "improvement_plan": [
    "specific improvement 1",
    "specific improvement 2",
    "specific improvement 3"
  ],
  "overall_feedback": "Final interviewer feedback."
}
```

The Streamlit interface converts this information into a structured performance dashboard.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      Candidate       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Upload Resume PDF  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Gemini File API   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Resume Analysis   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Generate Question 1  │
                         └──────────┬───────────┘
                                    │
                                    ▼
              ┌──────────────────────────────────────────┐
              │              INTERVIEW LOOP              │
              │                                          │
              │  ┌────────────────┐  ┌────────────────┐ │
              │  │    Webcam      │  │   Microphone   │ │
              │  └───────┬────────┘  └───────┬────────┘ │
              │          │                   │          │
              │          ▼                   ▼          │
              │  ┌────────────────┐  ┌────────────────┐ │
              │  │ Face Detection │  │ Speech-to-Text │ │
              │  │   OpenCV       │  │                │ │
              │  └───────┬────────┘  └───────┬────────┘ │
              │          │                   │          │
              │          ▼                   ▼          │
              │  ┌────────────────┐  ┌────────────────┐ │
              │  │    Emotion     │  │    Transcript  │ │
              │  │ Recognition    │  │                │ │
              │  └────────────────┘  └───────┬────────┘ │
              │                              │          │
              │                              ▼          │
              │                    ┌────────────────┐  │
              │                    │ Submit Answer  │  │
              │                    └───────┬────────┘  │
              └────────────────────────────┼───────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Gemini Answer       │
                                │ Evaluation          │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Interview History   │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Adaptive Question   │
                                │ Generation          │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │ 5 Questions    │
                                  │ Completed      │
                                  └───────┬────────┘
                                          │
                                          ▼
                                ┌─────────────────────┐
                                │ Final AI Report     │
                                └─────────────────────┘
```

---

# 🔁 Complete Application Workflow

```text
1. Launch Application
        ↓
2. Upload Resume
        ↓
3. Resume Uploaded to Gemini
        ↓
4. Gemini Analyzes Resume
        ↓
5. Generate First Technical Question
        ↓
6. Candidate Answers Using Microphone
        ↓
7. Speech Converted to Text
        ↓
8. Candidate Submits Answer
        ↓
9. Gemini Evaluates Answer
        ↓
10. Answer + Evaluation Stored
        ↓
11. Gemini Generates Next Question
        ↓
12. Repeat Until Question 5
        ↓
13. Generate Final Interview Report
        ↓
14. Display Performance Dashboard
```

---

# 🧩 Application Components

## Frontend

Built using:

```text
Streamlit
```

The interface is divided into two major sections.

### Left Side

```text
📷 Your Interview

Webcam
   ↓
Live Video
   ↓
Facial Emotion Detection
```

### Right Side

```text
🤖 AI Interviewer

Resume Upload
     ↓
Interview Question
     ↓
Speech-to-Text
     ↓
Transcript
     ↓
Submit Answer
```

---

# 🗂️ Session State Management

Since Streamlit reruns the application whenever users interact with the interface, the application uses `st.session_state` to maintain interview progress.

The application stores:

```text
interview_started
interview_finished
question_number
question
resume_file
answers
evaluations
final_report
current_answer
```

This allows the interview to continue correctly across Streamlit reruns.

---

# 🔄 Interview State Flow

```text
                    Start
                      │
                      ▼
              Resume Uploaded
                      │
                      ▼
              Interview Started
                      │
                      ▼
                 Question 1
                      │
                      ▼
              Submit Answer
                      │
                      ▼
              AI Evaluation
                      │
                      ▼
                 Question 2
                      │
                     ...
                      │
                      ▼
                 Question 5
                      │
                      ▼
             Interview Finished
                      │
                      ▼
              Final AI Report
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Streamlit** | Web application and UI |
| **Google Gemini API** | AI interviewer, evaluation and report generation |
| **Google GenAI SDK** | Gemini API integration |
| **OpenCV** | Face detection and webcam image processing |
| **TensorFlow** | Deep learning framework |
| **Keras** | Emotion recognition model |
| **Hugging Face Hub** | Pretrained model download |
| **Streamlit-WebRTC** | Real-time webcam streaming |
| **Streamlit-Mic-Recorder** | Speech-to-text |
| **NumPy** | Numerical and image processing |
| **python-dotenv** | Environment variable management |
| **Git/GitHub** | Version control and project hosting |

---

# 📦 Main Python Libraries

The application uses libraries including:

```text
streamlit
streamlit-webrtc
streamlit-mic-recorder
av
opencv-python
numpy
huggingface-hub
tensorflow
python-dotenv
google-genai
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📁 Project Structure

```text
AI-Mock-Interview/
│
├── interview_final.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
├── .env
│
├── temp_resume.pdf
│
└── venv/
```

### `interview_final.py`

Main application containing:

- Streamlit UI
- Gemini integration
- Resume processing
- Interview logic
- Adaptive question generation
- Speech-to-text
- Webcam streaming
- Face detection
- Emotion recognition
- Answer evaluation
- Final report generation

### `requirements.txt`

Contains the Python dependencies required by the application.

### `.env`

Stores the Gemini API key for local development.

### `temp_resume.pdf`

Temporary local copy of the uploaded resume used for Gemini file upload.

### `venv/`

Python virtual environment used for local development.

---

# ⚙️ Installation & Setup

## Prerequisites

Make sure you have:

- Python 3.10+
- Git
- Webcam
- Microphone
- Google Gemini API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Move into the project:

```bash
cd AI-Mock-Interview
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔑 Gemini API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

The application loads the API key using environment variables.

For local development:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
```

---

# 🔒 API Key Security

Never commit your Gemini API key to GitHub.

Recommended `.gitignore`:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
temp_resume.pdf
```

If an API key is accidentally pushed to a public repository:

1. Revoke the exposed key.
2. Generate a new key.
3. Remove the secret from the repository history if necessary.
4. Update your local `.env`.

---

# ▶️ Running the Application

Activate your virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Run Streamlit:

```powershell
streamlit run interview_final.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🎯 How To Use

## Step 1 — Upload Resume

Upload your resume as a PDF.

---

## Step 2 — Start Interview

Click:

```text
🚀 Start Interview
```

The application uploads the resume and asks Gemini to generate the first personalized technical question.

---

## Step 3 — Allow Camera & Microphone

Allow browser permissions for:

- Camera
- Microphone

The webcam will display on the left side.

---

## Step 4 — Answer

Click:

```text
🎤 Start Speaking
```

Speak your answer and stop the recording.

The generated transcript will appear in the answer section.

---

## Step 5 — Submit

Click:

```text
📤 Submit Answer
```

Gemini evaluates the answer.

---

## Step 6 — Continue

The system generates the next question based on the interview history.

---

## Step 7 — Complete 5 Questions

The interview continues until all five questions are completed.

---

## Step 8 — View Final Report

After Question 5, the application generates the final performance report.

---

# 📊 Example Final Report

```text
🎉 Interview Completed

Overall Score
82/100

Performance Breakdown

Technical Knowledge     8.5/10
Communication           7.8/10
Problem Solving         8.4/10
Answer Relevance        8.1/10

Strengths
✓ Good understanding of core concepts
✓ Relevant project examples
✓ Strong problem-solving approach

Areas to Improve
• Improve depth of technical explanations
• Structure answers more clearly
• Provide more implementation details

Improvement Plan
1. Practice explaining technical concepts
2. Revise core CS fundamentals
3. Practice project-based interview questions

Interviewer Feedback
Overall performance was strong...
```

---

# 🧪 Error Handling

The application includes retry handling for temporary Gemini availability issues.

The Gemini helper retries temporary `503 / UNAVAILABLE` errors using increasing delays.

```text
Attempt 1
   ↓
Wait 1 second
   ↓
Attempt 2
   ↓
Wait 2 seconds
   ↓
Attempt 3
```

This helps handle temporary AI service availability problems without immediately failing the interview.

---

# 🧠 Prompt Engineering

The application uses carefully designed prompts for different stages of the interview.

## Resume Question Prompt

The AI is instructed to:

- Analyze the resume
- Focus on actual technical experience
- Generate one question
- Avoid generic questions
- Test actual technical understanding

---

## Evaluation Prompt

The AI is instructed to evaluate:

```text
Technical Correctness
Relevance
Clarity
Depth
Completeness
```

and provide:

```text
Score
Strengths
Weaknesses
Improvement Suggestions
```

---

## Adaptive Question Prompt

The AI receives the previous interview history and is instructed to:

- Consider previous answers
- Ask deeper follow-ups for weak areas
- Increase difficulty when the candidate performs strongly
- Avoid repeating questions
- Cover different technical areas

Potential question categories include:

```text
Projects
Technical Skills
Internships
Problem Solving
System / Design Thinking
Technical Decision Making
Behavioral Situations
```

---

# 🧮 Interview Scoring

Individual answer scores are provided on a:

```text
0 – 10
```

scale.

The final overall score is generated on a:

```text
0 – 100
```

scale.

The application also categorizes overall performance as:

```text
80+  → Excellent
70+  → Good
60+  → Fair
Below 60 → Needs Improvement
```

---

# 🌐 Deployment

The application can be deployed using **Streamlit Community Cloud**.

## Deployment Steps

### 1. Push the project to GitHub

```bash
git add .
git commit -m "Add AI Mock Interview application"
git push origin main
```

### 2. Open Streamlit Community Cloud

Connect your GitHub repository.

### 3. Select the Main File

Use:

```text
interview_final.py
```

### 4. Configure Secrets

Instead of uploading `.env`, configure:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

in Streamlit Secrets.

### 5. Deploy

Start the Streamlit application.

---


### Speech Recognition

Speech-to-text accuracy can vary depending on:

- Microphone quality
- Accent
- Background noise
- Internet connection
- Speech clarity

### Generative AI

Gemini-generated questions and evaluations may occasionally be:

- Inaccurate
- Subjective
- Repetitive
- Overly strict or lenient

The AI evaluation should therefore be treated as interview-practice feedback rather than an authoritative assessment.

---

## Streamlit Session State

Streamlit reruns the application after interactions.

Maintaining the interview state required careful use of:

```python
st.session_state
```

to preserve:

- Current question
- Question number
- Resume
- Answers
- Evaluations
- Interview status
- Final report

---

## Webcam Processing

Real-time webcam processing required integration between:

```text
Streamlit
      +
Streamlit-WebRTC
      +
OpenCV
      +
TensorFlow/Keras
```

---

## Emotion Model Input Processing

The pretrained model required webcam faces to be transformed into the correct format:

```text
Webcam Face
     ↓
Grayscale
     ↓
48 × 48
     ↓
Float32
     ↓
Normalize /255
     ↓
Reshape
     ↓
(1, 48, 48, 1)
     ↓
Model Prediction
```

---

## Adaptive Interview Logic

The interview needed to maintain a complete history of:

```text
Question
+
Candidate Answer
+
AI Evaluation
```

This history is then provided to Gemini when generating the next question.

---

# 📚 What I Learned

This project provided hands-on experience with:

### Generative AI

- Gemini API integration
- Prompt engineering
- AI-based evaluation
- Adaptive question generation
- Structured JSON generation

### Machine Learning

- Using pretrained deep-learning models
- Model inference
- Facial-expression classification

### Computer Vision

- Webcam processing
- Face detection
- OpenCV
- Haar Cascades
- Image preprocessing

### Streamlit

- Interactive UI development
- Session state
- File uploads
- WebRTC integration
- Real-time components

### Speech Processing

- Microphone integration
- Speech-to-text
- Transcript handling

### Software Development

- API integration
- Error handling
- Retry mechanisms
- Environment variables
- Git/GitHub
- Deployment

---

# 🏆 Project Highlights

```text
🤖 AI-powered technical interviewer
📄 Resume-based personalized questions
🔄 Adaptive interview flow
🎤 Speech-to-text answers
🧠 AI-powered answer evaluation
😊 Real-time facial-expression recognition
📊 Detailed final performance report
🌐 Interactive Streamlit interface
```

---

# 🎓 Use Cases

## Students

Practice technical interviews before campus placements.

## Job Seekers

Practice interviews based on their actual resumes.

## Software Developers

Practice questions related to projects, technologies, and development experience.

## Interview Preparation

Identify weaknesses and improve technical communication.

## Self Assessment

Get structured AI-generated feedback after completing an interview.

---

# 🔮 Future Vision

The long-term goal is to evolve this project into a complete AI-powered interview preparation platform.

```text
                    AI Interview Platform
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
       Technical        Behavioral       Coding
       Interview        Interview       Interview
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
                    AI Evaluation
                            │
                            ▼
                  Performance Analytics
                            │
                            ▼
                 Personalized Feedback
                            │
                            ▼
                  Learning Recommendations
```

---

# 🛡️ Responsible AI Use

This project is designed for **educational and interview-practice purposes**.

AI-generated scores and feedback should be considered guidance rather than an objective measurement of a candidate's abilities.

Facial-expression predictions should **not** be used for:

- Hiring decisions
- Personality assessment
- Mental-state assessment
- Psychological diagnosis
- Determining candidate confidence
- Rejecting or selecting candidates

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

### Fork the repository

```bash
git fork
```

### Clone it

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Create a branch

```bash
git checkout -b feature/new-feature
```

### Make your changes

### Commit

```bash
git add .
git commit -m "Add new feature"
```

### Push

```bash
git push origin feature/new-feature
```

Then create a Pull Request.

---

# ⭐ Support

If you found this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

# 👨‍💻 Author

## Shivam Raj

Computer Science & Engineering Student

### Interests

- 🤖 Generative AI
- 🧠 Machine Learning
- 🔗 LangChain
- 🔗 LangGraph
- 🌐 Full-Stack Development
- 📊 AI Applications
- 💻 Software Development

---

# 📜 License

This project is intended for **educational and personal development purposes**.

---

## 🙌 Thank You

Thanks for checking out the **AI-Powered Mock Interview** project!

If you have suggestions, ideas, or improvements, feel free to contribute.
