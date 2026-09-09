# 🤖 AI-Powered Mock Interview

An AI-powered technical mock interview platform built with **Python and Streamlit** that simulates a real interview experience.

The application analyzes a candidate's resume, generates personalized technical questions using **Google Gemini**, accepts spoken answers through a microphone, evaluates responses, detects facial expressions through the webcam, and generates a detailed final performance report.

---

## 📌 Overview

Preparing for technical interviews can be difficult without realistic practice and personalized feedback.

This project provides an interactive mock interview environment where an AI interviewer conducts a **5-question technical interview** based on the candidate's resume.

The system combines:

- Generative AI
- Resume analysis
- Adaptive questioning
- Speech-to-text
- Facial emotion recognition
- AI-based answer evaluation
- Performance analytics

The goal is to provide candidates with a more realistic and personalized interview-practice experience.

---

## ✨ Features

### 📄 Resume-Based Interview

Candidates can upload their resume in PDF format.

The AI analyzes the resume to understand:

- Technical skills
- Projects
- Education
- Experience
- Technologies used
- Candidate background

The first interview question is then generated based on the candidate's profile.

---

### 🤖 AI Technical Interviewer

Google Gemini acts as the AI interviewer.

It can:

- Analyze the candidate's resume
- Generate technical questions
- Ask questions based on the candidate's skills and projects
- Evaluate candidate responses
- Generate adaptive follow-up questions
- Produce a final interview report

The interview is designed to be dynamic instead of simply asking a predefined list of questions.

---

### 🔄 Adaptive Question Generation

Each question can be generated using the context of the previous interview.

The AI considers:

- Resume information
- Previous questions
- Candidate answers
- Previous evaluations

This allows the interview to adapt to the candidate's responses.

---

### 🎤 Speech-to-Text

Candidates can answer questions using their microphone.

The speech-to-text functionality converts spoken responses into text, which can then be reviewed and submitted for AI evaluation.

---

### 🧠 AI Answer Evaluation

After submitting an answer, Gemini evaluates the response.

The evaluation considers factors such as:

- Technical knowledge
- Answer relevance
- Communication
- Problem-solving ability
- Overall answer quality

The candidate receives feedback for each response.

---

### 😊 Facial Emotion Detection

The application uses the webcam to analyze facial expressions during the interview.

The emotion-recognition pipeline uses:

- OpenCV
- TensorFlow/Keras
- A pretrained facial-expression recognition model

The system can detect:

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Surprise

The detected emotion and confidence are displayed alongside the webcam feed.

> **Note:** Facial emotion detection is provided as an experimental feature and should not be treated as a reliable psychological or hiring assessment.

---

### 📊 Final Performance Report

After completing all 5 questions, the application generates a detailed performance report.

The report includes:

- Overall Score
- Technical Knowledge
- Communication
- Problem Solving
- Answer Relevance
- Strengths
- Weaknesses
- Improvement Plan
- Overall Feedback
- Question-by-question analysis

---

### 🔁 Interview Restart

After completing an interview, candidates can start another interview and upload a new resume.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │    Candidate        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Upload Resume     │
                         │       (PDF)         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Google Gemini     │
                         │   Resume Analysis   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Generate Question 1 │
                         └──────────┬──────────┘
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │              Interview Loop             │
              │                                         │
              │  ┌──────────────┐   ┌───────────────┐  │
              │  │  Webcam      │   │  Microphone   │  │
              │  │  Feed        │   │  Answer       │  │
              │  └──────┬───────┘   └───────┬───────┘  │
              │         │                   │          │
              │         ▼                   ▼          │
              │  ┌──────────────┐   ┌───────────────┐  │
              │  │   Emotion    │   │ Speech-to-    │  │
              │  │  Detection   │   │    Text       │  │
              │  └──────────────┘   └───────┬───────┘  │
              │                             │          │
              │                             ▼          │
              │                    ┌────────────────┐  │
              │                    │ Submit Answer  │  │
              │                    └───────┬────────┘  │
              │                            │           │
              └────────────────────────────┼───────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │   Gemini Evaluation │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Generate Next       │
                                │ Adaptive Question   │
                                └──────────┬──────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ 5 Questions     │
                                  │ Completed       │
                                  └────────┬────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Final Performance   │
                                │       Report        │
                                └─────────────────────┘
