import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import json

# Page tab settings
st.set_page_config(page_title="AI On-Screen Marking System", layout="wide")

# --- ✨ PREMIUM MODERN MINIMALIST DARK THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700&display=swap');
    
    .stApp {
        background-color: #12141c;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes smoothSlide {
        0% { opacity: 0; transform: translateY(6px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .element-container, .stMarkdown, .stButton, div[data-testid="stExpander"] {
        animation: smoothSlide 0.4s ease-out forwards;
    }
    
    h1 {
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(45deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        padding-bottom: 10px;
    }
    
    h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #818cf8 !important;
        font-weight: 600 !important;
    }
    
    label[data-testid="stWidgetLabel"] p {
        color: #f8fafc !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        background-color: rgba(99, 102, 241, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 8px !important;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    div[data-testid="stTextArea"] textarea, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stFileUploader"] {
        background-color: #1e2230 !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        color: #10b981 !important;
        font-size: 3.2rem !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stExpander"] {
        background-color: #1e2230 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    .stAlert {
        background-color: #1e2230 !important;
        border-left: 5px solid #4f46e5 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTOMATIC API KEY LOADING FROM SECRETS ---
# Yeh line automatic Streamlit cloud ke backend se tumhari key utha legi!
try:
    api_key = st.secrets["GEMINI_KEY"]
except Exception:
    api_key = None

# --- MAIN UI ---
st.title("🎯 AI On-Screen Marking System")
st.write("Professional Evaluation Dashboard — Powered by Gemini AI")

# --- SIDEBAR: CLEAN & SIMPLE ---
st.sidebar.header("⚙️ Settings")
model_choice = st.sidebar.selectbox("Select Model Brain:", ["gemini-2.5-flash", "gemini-2.5-pro"])
st.sidebar.markdown("---")
st.sidebar.success("🔑 API Key Loaded Automatically!")

# Core Prompt Logic
SYSTEM_PROMPT = """
You are an expert Board Exam Evaluator with 20+ years of experience grading high-stakes secondary and senior secondary school examinations (specifically specializing in Mathematics, Physics, and Chemistry). Your core mission is to grade student answers with extreme accuracy, absolute lack of bias, and a strict adherence to partial-marking (step-marking) rules.

Output MUST be valid JSON data matching this schema:
{
  "total_marks_awarded": 1.5,
  "max_marks": 2.0,
  "step_by_step_breakdown": [
    {
      "step_number": 1,
      "description": "Step detail",
      "expected_content": "What was required",
      "student_content": "What student wrote",
      "marks_allocated": 0.5,
      "marks_awarded": 0.5,
      "feedback": "Reasoning"
    }
  ],
  "final_summary": "Constructive overview text"
}
"""

# --- MAIN INTERFACE: INPUT FIELDS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Exam Parameters")
    question = st.text_area("1. Paste the Exam Question:", 
                            value="An object of mass 2 kg is moving with a velocity of 5 m/s. Calculate its kinetic energy.")
    
    max_marks = st.number_input("2. Enter Max Marks:", min_value=1, max_value=100, value=2)
    
    marking_scheme = st.text_area("3. Paste the Official Marking Scheme Rubric:",
                                  value="- Correct formula: KE = 0.5 * m * v^2 (+0.5 marks)\n- Correct substitution: 0.5 * 2 * 5^2 (+0.5 marks)\n- Correct numerical value calculation: 25 (+0.5 marks)\n- Correct SI Unit (Joules or J): (+0.5 marks)")
    
    uploaded_file = st.file_uploader("4. Upload Student Handwritten Answer Sheet Image:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Student Paper", use_container_width=True)

# --- BACKEND EVALUATION EXECUTION ---
with col2:
    st.subheader("⚡ Live Evaluation Report")
    
    if st.button("🚀 Run Digital Checking"):
        if not api_key:
            st.error("🔑 API Key configuration missing! Please add GEMINI_KEY in Streamlit Cloud Secrets.")
        elif not uploaded_file:
            st.error("Please upload an image of the student's answer paper.")
        else:
            with st.spinner("Analyzing handwriting and verification steps..."):
                try:
                    client = genai.Client(api_key=api_key)
                    img_data = Image.open(uploaded_file)
                    
                    user_query = f"""
                    [Inputs Data]
                    - Question: {question}
                    - Max Marks: {max_marks}
                    - Official Marking Scheme: {marking_scheme}
                    
                    Evaluate this sheet using your system guardrails.
                    """
                    
                    config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                    
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=[img_data, user_query],
                        config=config
                    )
                    
                    result_json = json.loads(response.text)
                    
                    st.success("Evaluation Completed Successfully!")
                    
                    score_col1, score_col2 = st.columns(2)
                    score_col1.metric("MARKS AWARDED", f"{result_json.get('total_marks_awarded')} / {result_json.get('max_marks')}")
                    
                    st.markdown("### 📝 STEP-BY-STEP BREAKDOWN")
                    for step in result_json.get("step_by_step_breakdown", []):
                        with st.expander(f"Step {step.get('step_number')}: {step.get('description')} ({step.get('marks_awarded')}/{step.get('marks_allocated')} Marks)"):
                            st.write(f"**Expected:** {step.get('expected_content')}")
                            st.write(f"**Student Wrote:** {step.get('student_content')}")
                            st.info(f"**AI Notes:** {step.get('feedback')}")
                            
                    st.markdown("### 🧐 SUMMARY FEEDBACK")
                    st.info(result_json.get("final_summary"))
                    
                except Exception as e:
                    st.error(f"An execution error occurred: {e}")
