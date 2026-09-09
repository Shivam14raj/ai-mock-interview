import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import streamlit_mic_recorder
import av
import cv2
import numpy as np

from huggingface_hub import hf_hub_download
from tensorflow.keras.models import load_model

import os
import re
import json
import time
from dotenv import load_dotenv
from google import genai




load_dotenv()

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)        



st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="🎤",
    layout="wide"
)




st.markdown("""
<style>
    .score-box {
        padding: 24px;
        border-radius: 18px;
        border: 1px solid rgba(128,128,128,.25);
        text-align: center;
        margin-bottom: 18px;
    }

    .big-score {
        font-size: 46px;
        font-weight: 800;
        margin: 0;
    }

    .score-label {
        font-size: 16px;
        opacity: .75;
    }

    .metric-card {
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,.25);
        min-height: 120px;
    }

    .metric-title {
        font-size: 14px;
        opacity: .7;
        margin-bottom: 6px;
    }

    .metric-score {
        font-size: 28px;
        font-weight: 750;
    }

    .section-title {
        margin-top: 25px;
    }

    .feedback-box {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,.20);
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)



# GEMINI HELPER


def generate_gemini(contents, retries=3, json_mode=False):
    """
    Calls Gemini with simple retry handling for temporary 503 errors.
    """

    for attempt in range(retries):
        try:
            config = None

            if json_mode:
                config = {
                    "response_mime_type": "application/json"
                }

            return client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
                config=config
            )

        except Exception as e:
            error_text = str(e)

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            ):
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            raise


# LOAD EMOTION MODEL


@st.cache_resource
def load_emotion_model():

    model_path = hf_hub_download(
        repo_id="lokeshkumar79/facial-emotion-recognition",
        filename="finalfacialemotionmodel.keras"
    )

    return load_model(model_path)


model = load_emotion_model()



# EMOTIONS


emotions = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]


# FACE DETECTOR


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)



# VIDEO PROCESSOR


class EmotionProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face = gray[
                y:y + h,
                x:x + w
            ]

            face = cv2.resize(
                face,
                (48, 48)
            )

            face = face.astype(
                "float32"
            ) / 255.0

            face = face.reshape(
                1,
                48,
                48,
                1
            )

            prediction = model.predict(
                face,
                verbose=0
            )

            emotion_index = np.argmax(
                prediction
            )

            emotion = emotions[
                emotion_index
            ]

            confidence = np.max(
                prediction
            )

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            text = (
                f"{emotion} "
                f"{confidence * 100:.1f}%"
            )

            cv2.putText(
                img,
                text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )



# SESSION STATE


defaults = {
    "interview_started": False,
    "interview_finished": False,
    "question_number": 0,
    "question": "",
    "resume_file": None,
    "answers": [],
    "evaluations": [],
    "final_report": None,
    "current_answer": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value



# RESET INTERVIEW


def reset_interview():

    st.session_state.interview_started = False
    st.session_state.interview_finished = False
    st.session_state.question_number = 0
    st.session_state.question = ""
    st.session_state.resume_file = None
    st.session_state.answers = []
    st.session_state.evaluations = []
    st.session_state.final_report = None
    st.session_state.current_answer = ""



# FINAL REPORT UI


def get_score_from_evaluation(text):

    match = re.search(
        r"(?:score|rating)[^\d]{0,20}(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*/\s*10\b",
        text
    )

    if match:
        return float(match.group(1))

    return None


def display_final_report():

    st.title("🎉 Interview Completed")

    st.caption(
        "Here is your complete AI-generated interview performance report."
    )

    report = st.session_state.final_report

    if not report:
        st.warning("Final report is not available yet.")
        return

    # --------------------------------------------------------
    # Overall score
    # --------------------------------------------------------

    overall = report.get("overall_score", 0)

    if overall >= 80:
        verdict = "Excellent"
    elif overall >= 70:
        verdict = "Good"
    elif overall >= 60:
        verdict = "Fair"
    else:
        verdict = "Needs Improvement"

    st.markdown(
        f"""
        <div class="score-box">
            <div class="big-score">{overall}/100</div>
            <div class="score-label">{verdict} Interview Performance</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Skill cards
    # --------------------------------------------------------

    st.markdown("## 📊 Performance Breakdown")

    cols = st.columns(4)

    metrics = [
        ("Technical Knowledge", report.get("technical_knowledge", 0)),
        ("Communication", report.get("communication", 0)),
        ("Problem Solving", report.get("problem_solving", 0)),
        ("Answer Relevance", report.get("answer_relevance", 0))
    ]

    for col, (title, score) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-score">{score}/10</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # Strengths / weaknesses
    # --------------------------------------------------------

    st.markdown("## 💪 Strengths")

    strengths = report.get("strengths", [])

    if strengths:
        for item in strengths:
            st.markdown(f"✅ {item}")
    else:
        st.write("No strengths provided.")

    st.markdown("## ⚠️ Areas to Improve")

    weaknesses = report.get("weaknesses", [])

    if weaknesses:
        for item in weaknesses:
            st.markdown(f"• {item}")
    else:
        st.write("No weaknesses provided.")

    # --------------------------------------------------------
    # Improvement plan
    # --------------------------------------------------------

    st.markdown("## 💡 Improvement Plan")

    improvements = report.get("improvement_plan", [])

    if improvements:
        for i, item in enumerate(improvements, 1):
            st.markdown(f"**{i}.** {item}")
    else:
        st.write("No improvement plan provided.")

    # --------------------------------------------------------
    # Overall feedback
    # --------------------------------------------------------

    st.markdown("## 🤖 Interviewer Feedback")

    st.info(
        report.get(
            "overall_feedback",
            "No overall feedback provided."
        )
    )

    # --------------------------------------------------------
    # Question-by-question analysis
    # --------------------------------------------------------

    st.markdown("## 📝 Question-by-Question Analysis")

    for i, item in enumerate(
        st.session_state.answers
    ):

        question = item["question"]
        answer = item["answer"]
        evaluation = st.session_state.evaluations[i]

        score = get_score_from_evaluation(
            evaluation
        )

        score_text = (
            f"{score}/10"
            if score is not None
            else "Evaluated"
        )

        with st.expander(
            f"Q{i + 1}  •  {score_text}"
        ):

            st.markdown("**Question**")
            st.write(question)

            st.markdown("**Your Answer**")
            st.write(answer)

            st.markdown("**AI Evaluation**")
            st.write(evaluation)

    st.divider()

    if st.button(
        "🔄 Take Interview Again",
        use_container_width=True
    ):
        reset_interview()
        st.rerun()


# ============================================================
# FINAL REPORT MODE
# ============================================================

# Once Q10 is complete, don't render the webcam/interview UI.
if st.session_state.interview_finished:

    if st.session_state.final_report is None:

        complete_history = ""

        for i in range(
            len(st.session_state.answers)
        ):

            complete_history += f"""
Question {i + 1}:
{st.session_state.answers[i]["question"]}

Candidate Answer:
{st.session_state.answers[i]["answer"]}

Evaluation:
{st.session_state.evaluations[i]}
"""

        final_prompt = f"""
You are an expert technical interviewer.

Analyze the candidate's complete 5-question mock interview.

Interview history:

{complete_history}

Return ONLY valid JSON.

Use exactly this structure:

{{
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
  "overall_feedback": "Concise but useful final interviewer feedback."
}}

Scoring rules:

- overall_score must be between 0 and 100.
- Other scores must be between 0 and 10.
- Judge the actual quality of the candidate's answers.
- Be honest and critical.
- Do not give high scores merely because the answers sound confident.
- Consider technical correctness, depth, relevance, clarity,
  problem solving and completeness.
"""

        try:

            with st.spinner(
                "🤖 Generating your final interview report..."
            ):

                response = generate_gemini(
                    final_prompt,
                    json_mode=True
                )

                report_text = response.text.strip()

                st.session_state.final_report = json.loads(
                    report_text
                )

                st.rerun()

        except Exception as e:

            st.error(
                "The AI service is temporarily busy or the report "
                "could not be generated."
            )

            st.caption(
                "Your 10 answers are already saved. "
                "Click below to try generating the report again."
            )

            if st.button(
                "🔁 Generate Report Again",
                use_container_width=True
            ):
                st.rerun()

            st.stop()

    display_final_report()
    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🎤 AI Mock Interview")

st.caption(
    "Resume-based AI interview with live facial-expression analysis"
)

st.divider()


# ============================================================
# TWO COLUMNS
# ============================================================

left, right = st.columns([1, 1])


# ============================================================
# LEFT SIDE - CAMERA + EMOTION
# ============================================================

with left:

    st.subheader("📷 Your Interview")

    webrtc_streamer(
        key="emotion-interview",
        video_processor_factory=EmotionProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )

    st.caption(
        "Your facial expression is analyzed locally "
        "using OpenCV and a pretrained emotion model."
    )


# ============================================================
# RIGHT SIDE - AI INTERVIEWER
# ============================================================

with right:

    st.subheader("🤖 AI Interviewer")

    # ========================================================
    # RESUME UPLOAD
    # ========================================================

    if not st.session_state.interview_started:

        resume = st.file_uploader(
            "Upload your resume",
            type=["pdf"]
        )

        if resume:

            st.success(
                "Resume uploaded successfully!"
            )

            st.info(
                "The AI will use your resume to create "
                "personalized interview questions."
            )

            if st.button(
                "🚀 Start Interview",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "AI is analyzing your resume..."
                    ):

                        with open(
                            "temp_resume.pdf",
                            "wb"
                        ) as f:
                            f.write(
                                resume.getbuffer()
                            )

                        resume_file = client.files.upload(
                            file="temp_resume.pdf"
                        )

                        st.session_state.resume_file = (
                            resume_file
                        )

                        response = generate_gemini(
                            [
                                resume_file,
                                """
                                You are an expert technical interviewer.

                                Analyze the candidate's resume carefully.

                                Start a technical mock interview.

                                Generate ONE interview question specifically
                                based on the candidate's resume.

                                The question can be based on:
                                - Projects
                                - Technical skills
                                - Internships
                                - Technologies
                                - Work experience

                                Do NOT ask generic questions such as:
                                "Tell me about yourself."

                                The question should test the candidate's
                                actual technical understanding.

                                Return ONLY the interview question.
                                """
                            ]
                        )

                        st.session_state.question = (
                            response.text.strip()
                        )

                        st.session_state.question_number = 1
                        st.session_state.interview_started = True

                        st.rerun()

                # except Exception:

                #     st.error(
                #         "Gemini is temporarily unavailable. "
                #         "Please try again in a few seconds."
                #     )
                except Exception as e:
                    st.error(f"Gemini error: {type(e).__name__}")
                    st.code(str(e))


    # ========================================================
    # INTERVIEW
    # ========================================================

    if st.session_state.interview_started:

        question_number = (
            st.session_state.question_number
        )

        st.divider()

        st.markdown(
            f"### Question {question_number} / 5"
        )

        st.progress(
            question_number / 5
        )

        st.info(
            st.session_state.question
        )

        # ----------------------------------------------------
        # Speech to text
        # ----------------------------------------------------

        st.markdown("### 🎤 Your Answer")

        st.caption(
            "Click the microphone, speak your answer, "
            "then stop recording."
        )

        spoken_text = (
            streamlit_mic_recorder.speech_to_text(
                language="en",
                start_prompt="🎤 Start Speaking",
                stop_prompt="⏹️ Stop Speaking",
                just_once=True,
                use_container_width=True,
                key=f"speech_{question_number}"
            )
        )

        if spoken_text:
            st.session_state.current_answer = spoken_text

        # ----------------------------------------------------
        # Transcript
        # ----------------------------------------------------

        if st.session_state.current_answer:

            st.text_area(
                "Transcript",
                value=st.session_state.current_answer,
                height=180,
                key=f"transcript_{question_number}"
            )

        # ----------------------------------------------------
        # Submit answer
        # ----------------------------------------------------

        if st.button(
            "📤 Submit Answer",
            use_container_width=True
        ):

            answer = st.session_state.get(
                "current_answer",
                ""
            )

            if not answer.strip():

                st.warning(
                    "Please record your answer first."
                )

            else:

                try:

                    with st.spinner(
                        "🤖 AI is analyzing your answer..."
                    ):

                        evaluation_prompt = f"""
You are an expert technical interviewer.

Interview Question:
{st.session_state.question}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Consider:
1. Technical correctness
2. Relevance
3. Clarity
4. Depth of understanding
5. Completeness

Give:
- Score out of 10
- Technical correctness
- Relevance
- Clarity
- Strengths
- Weaknesses
- Specific improvement suggestions

Be honest and critical.

Do not give a high score simply because the answer sounds confident.

Keep the evaluation concise.
"""

                        evaluation_response = generate_gemini(
                            evaluation_prompt
                        )

                        evaluation = (
                            evaluation_response.text.strip()
                        )

                        # Save answer only AFTER successful evaluation.
                        # This prevents duplicate/lost records if Gemini
                        # returns a temporary 503 error.
                        st.session_state.answers.append({
                            "question":
                                st.session_state.question,
                            "answer":
                                answer
                        })

                        st.session_state.evaluations.append(
                            evaluation
                        )

                        if question_number == 5:

                            st.session_state.interview_finished = True

                        else:

                            history = ""

                            for i in range(
                                len(
                                    st.session_state.answers
                                )
                            ):

                                history += f"""
Question {i + 1}:
{st.session_state.answers[i]["question"]}

Candidate Answer:
{st.session_state.answers[i]["answer"]}

Evaluation:
{st.session_state.evaluations[i]}
"""

                            next_question_prompt = f"""
You are conducting a technical mock interview.

The candidate's resume is attached.

This is question {question_number + 1} of 5.

Previous interview history:

{history}

Generate ONE new interview question.

The question must be relevant to the candidate's resume.

Consider the candidate's previous answers.

If the candidate showed weak understanding in an area,
ask a deeper follow-up question.

If the candidate showed strong understanding,
increase the difficulty.

Do NOT repeat previous questions.

Mix questions across:
- Projects
- Technical skills
- Internships
- Problem solving
- System/design thinking
- Technical decision making
- Behavioral situations

Return ONLY the next question.
"""

                            next_response = generate_gemini(
                                [
                                    st.session_state.resume_file,
                                    next_question_prompt
                                ]
                            )

                            st.session_state.question = (
                                next_response.text.strip()
                            )

                            st.session_state.question_number += 1

                        st.session_state.current_answer = ""

                    st.rerun()

                except Exception:

                    st.error(
                        "Gemini is temporarily busy. "
                        "Your answer has NOT been submitted. "
                        "Please click Submit again in a few seconds."
                    )
