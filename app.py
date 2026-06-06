import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import json

# Page tab settings
st.set_page_config(page_title="AI On-Screen Marking System", layout="wide")

# --- ✨ IMAGE_F2AB05.PNG INSPIRED FUTURISTIC NEON PURPLE THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;700&display=swap');
    
    /* Pitch Black Background like image_f2ab05.png */
    .stApp {
        background-color: #09090b !important; 
        color: #e4e4e7 !important; 
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes smoothSlide {
        0% { opacity: 0; transform: translateY(6px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .element-container, .stMarkdown, .stButton, div[data-testid="stExpander"] {
        animation: smoothSlide 0.4s ease-out forwards;
    }
    
    /* Heading with glowing electric purple gradient effect */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: linear-gradient(135deg, #ffffff 60%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        padding-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f4f4f5 !important; 
        font-weight: 600 !important;
    }
    
    /* Input Labels customized with deep dark background and neon purple border glow */
    label[data-testid="stWidgetLabel"] p {
        color: #e9d5ff !important; 
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        background-color: rgba(168, 85, 247, 0.08); 
        padding: 4px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 8px !important;
        border: 1px solid rgba(168, 85, 247, 0.25);
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.05);
    }
    
    /* Sleek Cyber Dark Input fields */
    div[data-testid="stTextArea"] textarea, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stFileUploader"] {
        background-color: #121217 !important; 
        color: #ffffff !important; 
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }
    div[data-testid="stTextArea"] textarea:focus, 
    div[data-testid="stNumberInput"] input:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.15) !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #030303 !important;
        border-right: 1px solid #18181b;
    }
    
    /* Exact Neon Electric Purple/Magenta Button from image_f2ab05.png */
    .stButton>button {
        background: linear-gradient(135deg, #a855f7, #c084fc) !important; 
        color: #ffffff !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: none !important;
        border-radius: 20px !important; /* Rounded pill style like 'Take Free Trial' */
        padding: 12px 24px !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
        transition: all 0.2s ease !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 28px rgba(168, 85, 247, 0.6) !important;
        background: linear-gradient(135deg, #b55fe6, #ca95ff) !important; 
    }
    
    /* Metric Value highlights matching the layout graphics */
    div[data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #d8b4fe !important; 
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
    }
    
    /* Clean Glassmorphic Style Breakdown Cards */
    div[data-testid="stExpander"] {
        background-color: #121217 !important;
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
    }
    
    .stAlert {
        background-color: #121217 !important;
        border-left: 5px solid #a855f7 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOADING KEYS FROM SECRETS ---
gemini_key = st.secrets.get("GEMINI_KEY", None)
groq_key = st.secrets.get("GROQ_API_KEY", None)
cohere_key = st.secrets.get("COHERE_API_KEY", None)

# --- MAIN UI ---
st.title("🎯 AI On-Screen Marking System")
st.write("Universal Digital Evaluation Framework — High Performance Matrix")

# --- SIDEBAR: CLEAN CONFIGURATION ---
st.sidebar.header("⚙️ System Control")
ai_provider = st.sidebar.selectbox("Select AI Brain Provider:", ["Google Gemini", "Groq Cloud (Llama 3)", "Cohere API"])

if ai_provider == "Google Gemini":
    model_choice = st.sidebar.selectbox("Select Model:", ["gemini-2.5-flash", "gemini-2.5-pro"])
elif ai_provider == "Groq Cloud (Llama 3)":
    model_choice = st.sidebar.selectbox("Select Model:", ["llama-3.2-11b-vision-preview"])
elif ai_provider == "Cohere API":
    model_choice = st.sidebar.selectbox("Select Model:", ["command-r-plus"])

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
    st.subheader("📋 Core Parameters")
    question = st.text_area("1. Paste the Exam Question:", 
                            value="An object of mass 2 kg is moving with a velocity of 5 m/s. Calculate its kinetic energy.")
    
    max_marks = st.number_input("2. Enter Max Marks:", min_value=1, max_value=100, value=2)
    
    marking_scheme = st.text_area("3. Paste the Official Marking Scheme Rubric:",
                                  value="- Correct formula: KE = 0.5 * m * v^2 (+0.5 marks)\n- Correct substitution: 0.5 * 2 * 5^2 (+0.5 marks)\n- Correct numerical value calculation: 25 (+0.5 marks)\n- Correct SI Unit (Joules or J): (+0.5 marks)")
    
    uploaded_file = st.file_uploader("4. Upload Student Handwritten Answer Sheet Image:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Student Paper", use_container_width=True)

# --- BACKEND MULTI-ENGINE EXECUTION ---
with col2:
    st.subheader("⚡ Live Matrix Analysis")
    
    if st.button("🚀 Run Digital Checking"):
        if not uploaded_file:
            st.error("Please upload an image of the student's answer paper.")
        else:
            user_query = f"[Inputs Data]\n- Question: {question}\n- Max Marks: {max_marks}\n- Official Marking Scheme: {marking_scheme}\n\nEvaluate this sheet using your system guardrails."
            result_json = None
            
            with st.spinner(f"Analyzing via {ai_provider}..."):
                try:
                    img_data = Image.open(uploaded_file)
                    
                    # --- ENGINE 1: GOOGLE GEMINI ---
                    if ai_provider == "Google Gemini":
                        if not gemini_key:
                            st.error("🔑 Gemini Key missing in Secrets!")
                        else:
                            client = genai.Client(api_key=gemini_key)
                            config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, response_mime_type="application/json", temperature=0.1)
                            response = client.models.generate_content(model=model_choice, contents=[img_data, user_query], config=config)
                            result_json = json.loads(response.text)
                    
                    # --- ENGINE 2: GROQ CLOUD ---
                    elif ai_provider == "Groq Cloud (Llama 3)":
                        if not groq_key:
                            st.error("🔑 Groq API Key missing in Secrets!")
                        else:
                            import groq
                            import base64
                            import io
                            
                            buffered = io.BytesIO()
                            img_data.save(buffered, format="JPEG")
                            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                            
                            groq_client = groq.Groq(api_key=groq_key)
                            response = groq_client.chat.completions.create(
                                model=model_choice,
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": SYSTEM_PROMPT},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": user_query},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                                    ]}
                                ]
                            )
                            result_json = json.loads(response.choices[0].message.content)

                    # --- ENGINE 3: COHERE API ---
                    elif ai_provider == "Cohere API":
                        if not cohere_key:
                            st.error("🔑 Cohere API Key missing in Secrets!")
                        else:
                            import cohere
                            cohere_client = cohere.ClientV2(api_key=cohere_key)
                            
                            full_text_prompt = f"{SYSTEM_PROMPT}\n\n[User Content to Evaluate]:\n{user_query}\n\nNote: Please return a strict JSON output matching the requested schema."
                            
                            response = cohere_client.chat(
                                model=model_choice,
                                response_format={"type": "json_object"},
                                messages=[{"role": "user", "content": full_text_prompt}]
                            )
                            result_json = json.loads(response.message.content[0].text)
                    
                    # --- DISPLAY RESULTS ---
                    if result_json:
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

