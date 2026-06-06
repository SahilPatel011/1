import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import json

# Page tab settings
st.set_page_config(page_title="AI On-Screen Marking System", layout="wide")

st.title("🎯 Next-Gen AI On-Screen Marking (OSM) Dashboard")
st.write("Upload a scanned answer sheet, provide the marking scheme, and let Gemini evaluate steps programmatically.")

# --- SIDEBAR: API KEY SETUP ---
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
model_choice = st.sidebar.selectbox("Select Model Brain:", ["gemini-2.5-pro", "gemini-2.5-flash"])

# Core Prompt Logic
SYSTEM_PROMPT = """
You are an expert Board Exam Evaluator with 20+ years of experience grading high-stakes secondary and senior secondary school examinations (specifically specializing in Mathematics, Physics, and Chemistry). Your core mission is to grade student answers with extreme accuracy, absolute lack of bias, and a strict adherence to partial-marking (step-marking) rules.

[Core Evaluation Rules]
1. STRICT STEP-MARKING: You must evaluate the student's response chronologically, step-by-step. Compare each step of the student's work to the Official Marking Scheme. Do not just look at the final answer.
2. PARTIAL CREDIT CONSERVATION: If a student makes a calculation mistake early on but uses the correct formula, award full marks for the formula step as per the marking scheme. If they carry forward that wrong number but perform the subsequent steps perfectly using correct logic, award partial marks for the correct logic. Do not penalize them twice for a single calculation error.
3. DIAGRAMS & SYMBOLS: Verify if required diagrams, units, or variables are present and correctly labeled.
4. HANDWRITING BIAS ELIMINATION: Ignore poor handwriting or messy crossings-out. Focus entirely on structural correctness.

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
    st.subheader("📋 Exam Parameters & Answer Sheet")
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
    st.subheader("⚡ Live AI Evaluation Report")
    
    if st.button("🚀 Run AI Digital Checking"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first!")
        elif not uploaded_file:
            st.error("Please upload an image of the student's answer paper.")
        else:
            with st.spinner("Gemini is reading handwriting and auditing calculations step-by-step..."):
                try:
                    # Initialize the official GenAI Client
                    client = genai.Client(api_key=api_key)
                    img_data = Image.open(uploaded_file)
                    
                    user_query = f"""
                    [Inputs Data]
                    - Question: {question}
                    - Max Marks: {max_marks}
                    - Official Marking Scheme: {marking_scheme}
                    
                    Evaluate this sheet using your system guardrails.
                    """
                    
                    # Force strict JSON formatting configuration
                    config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                    
                    # Trigger the Multimodal Engine
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=[img_data, user_query],
                        config=config
                    )
                    
                    # Parse and clean output data
                    result_json = json.loads(response.text)
                    
                    # --- DISPLAYING BEAUTIFUL METRICS & INTERFACE ---
                    st.success("Paper Checked Successfully!")
                    
                    # Score Callout Box
                    score_col1, score_col2 = st.columns(2)
                    score_col1.metric("Marks Awarded", f"{result_json.get('total_marks_awarded')} / {result_json.get('max_marks')}")
                    
                    st.markdown("### 📝 Step-by-Step Marking Breakdown")
                    for step in result_json.get("step_by_step_breakdown", []):
                        with st.expander(f"Step {step.get('step_number')}: {step.get('description')} ({step.get('marks_awarded')}/{step.get('marks_allocated')} Marks)"):
                            st.write(f"**Expected:** {step.get('expected_content')}")
                            st.write(f"**Student Wrote:** {step.get('student_content')}")
                            st.info(f"**Examiner Notes:** {step.get('feedback')}")
                            
                    st.markdown("### 🧐 Teacher's Final Summary Feedback")
                    st.info(result_json.get("final_summary"))
                    
                except Exception as e:
                    st.error(f"An execution error occurred: {e}")
