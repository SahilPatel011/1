import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import json

# Page tab settings
st.set_page_config(page_title="AI On-Screen Marking System", layout="wide")

# --- 🔥 SUPER COOL DARK CYBERPUNK THEME & ANIMATIONS ---
st.markdown("""
    <style>
    /* Global App Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Space+Grotesk:wght@400;600&display=swap');
    
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Smooth Fade-in Animation for everything */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .element-container, .stMarkdown, .stButton, div[data-testid="stExpander"] {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    /* Headers Customization with Sci-Fi Font */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00f2fe !important;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.3);
    }
    
    /* Sidebar Dark Cyber styling */
    section[data-testid="stSidebar"] {
        background-color: #05070c !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Glowing Run Button Customization */
    .stButton>button {
        background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
        color: #05070c !important;
        font-weight: bold !important;
        font-family: 'Orbitron', sans-serif !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 6px 25px rgba(0, 242, 254, 0.8) !important;
    }
    
    /* Metric Score Box Card */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #00ff87 !important;
        font-size: 3rem !important;
        text-shadow: 0 0 15px rgba(0, 255, 135, 0.4);
    }
    
    /* Neat Glowing Cards for Results and Expanders */
    div[data-testid="stExpander"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
    }
    
    /* Custom alerts/boxes colors */
    .stAlert {
        background-color: #111827 !important;
        border-left: 5px solid #00f2fe !important;
        color: #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MAIN UI ---
st.title("🎯 NEXT-GEN AI OSM DASHBOARD")
st.write("Cyberpunk Matrix Edition — Autonomous Script Audit Engine")

# --- SIDEBAR: API KEY SETUP ---
st.sidebar.header("🔑 SECURE CONFIG")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
model_choice = st.sidebar.selectbox("Select Model Brain:", ["gemini-2.5-flash", "gemini-2.5-pro"])

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
    st.subheader("📋 PARAMETERS")
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
    st.subheader("⚡ LIVE AI REPORT")
    
    if st.button("🚀 EXECUTE DIGITAL CHECKING"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first!")
        elif not uploaded_file:
            st.error("Please upload an image of the student's answer paper.")
        else:
            with st.spinner("QUANTUM COMPUTING IN PROGRESS: Reading handwriting and auditing calculations..."):
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
                    
                    st.success("SYSTEM AUDIT COMPLETE!")
                    
                    score_col1, score_col2 = st.columns(2)
                    score_col1.metric("MARKS AWARDED", f"{result_json.get('total_marks_awarded')} / {result_json.get('max_marks')}")
                    
                    st.markdown("### 📝 STEP-BY-STEP ANALYSIS")
                    for step in result_json.get("step_by_step_breakdown", []):
                        with st.expander(f"Step {step.get('step_number')}: {step.get('description')} ({step.get('marks_awarded')}/{step.get('marks_allocated')} Marks)"):
                            st.write(f"**Expected:** {step.get('expected_content')}")
                            st.write(f"**Student Wrote:** {step.get('student_content')}")
                            st.info(f"**AI Notes:** {step.get('feedback')}")
                            
                    st.markdown("### 🧐 EVALUATOR SUMMARY")
                    st.info(result_json.get("final_summary"))
                    
                except Exception as e:
                    st.error(f"An execution error occurred: {e}")
                  
