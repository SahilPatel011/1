import streamlit as st
from google import genai
from google.genai import types
import json

# Page settings
st.set_page_config(page_title="GamerScript AI — Hyper-Retention Matrix", layout="wide")

# --- ✨ CYBERPUNK FUTURISTIC DASHBOARD CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600&family=Plus+Jakarta+Sans:wght=500;700&display=swap');
    
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
    
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: linear-gradient(135deg, #ffffff 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        padding-bottom: 10px;
    }
    
    h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #a855f7 !important; 
        font-weight: 600 !important;
    }
    
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
    }
    
    div[data-testid="stTextArea"] textarea, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #121217 !important; 
        color: #ffffff !important; 
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #030303 !important;
        border-right: 1px solid #18181b;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #a855f7, #c084fc) !important; 
        color: #ffffff !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: none !important;
        border-radius: 20px !important; 
        padding: 12px 24px !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
        transition: all 0.2s ease !important;
        width: 100%;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 28px rgba(168, 85, 247, 0.6) !important;
    }
    
    div[data-testid="stExpander"] {
        background-color: #121217 !important;
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Loading Keys
gemini_key = st.secrets.get("GEMINI_KEY", None)

st.title("🎮 GamerScript AI Engine")
st.write("Hyper-Retention Scripting Suite for Next-Gen Creators")

# Sidebar
st.sidebar.header("🕹️ Control Room")
ai_provider = st.sidebar.selectbox("Select Model Engine:", ["Google Gemini", "Groq Cloud"])
model_choice = "gemini-2.5-flash" if ai_provider == "Google Gemini" else "llama-3.2-11b-vision-preview"

# System Prompt instructing structured output
SYSTEM_PROMPT = """
You are a master YouTube Gaming Consultant and Retention Scriptwriter who has worked with top-tier gaming creators (like MrBeast Gaming, Dream, Mythpat). You know exactly how to write scripts that keep average view duration (AVD) above 70%.

Output MUST be valid JSON matching this exact format:
{
  "title_ideas": ["Title 1", "Title 2", "Title 3"],
  "thumbnail_concept": "Detailed graphic prompt for thumbnail design",
  "intro_hook": "The first 30 seconds of high-energy script text with visual/sound cues",
  "body_pacing": [
    {"segment": "Part 1 Name", "script_text": "Commentary text...", "editing_cue": "[Sound effect/Zoom cue]"}
  ],
  "outro_retention": "High-retention end screen call-to-action script text"
}
"""

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Gameplay Specs")
    video_idea = st.text_area("1. What is the video challenge or concept?", 
                              value="I tried surviving 100 days in a world where everything explodes when I touch it.")
    
    game_title = st.selectbox("2. Select the Game:", ["Minecraft", "GTA V", "BGMI / Valorant", "Horror Game (Granny/Phasmophobia)", "Custom / Indie Game"])
    video_style = st.selectbox("3. Video Commentary Vibe:", ["Hyper-Energetic Challenge", "Funny/Rage Quit", "Story Roleplay", "Deep Lore/Documentary"])
    duration = st.number_input("4. Estimated Target Video Length (Minutes):", min_value=2, max_value=30, value=8)

with col2:
    st.subheader("⚡ Live Telemetry Output")
    
    if st.button("🚀 Synthesize Script Matrix"):
        if not gemini_key:
            st.error("🔑 API Key Missing in Secrets!")
        else:
            user_query = f"Game: {game_title}\nStyle: {video_style}\nConcept Idea: {video_idea}\nTarget Length: {duration} mins\nGenerate the complete structured gaming script workflow."
            
            with st.spinner("Processing multi-agent pipeline logic..."):
                try:
                    client = genai.Client(api_key=gemini_key)
                    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, response_mime_type="application/json", temperature=0.7)
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=[user_query], config=config)
                    
                    result_json = json.loads(response.text)
                    
                    st.success("Script System Optimized!")
                    
                    # 1. Titles & Thumbnails
                    st.markdown("### 🧲 CTR Optimization Packages")
                    cols_t = st.columns(3)
                    titles = result_json.get("title_ideas", ["Title", "Title", "Title"])
                    for idx, t in enumerate(titles[:3]):
                        cols_t[idx].code(t, language="text")
                    st.info(f"🎨 **Thumbnail Concept:** {result_json.get('thumbnail_concept')}")
                    
                    # 2. Intro Hook
                    st.markdown("### 🔥 30-Sec Ultra-Hook (Crucial for Retention)")
                    st.warning(result_json.get("intro_hook"))
                    
                    # 3. Body Script
                    st.markdown("### 📝 Main Gameplay Commentary Pipeline")
                    for part in result_json.get("body_pacing", []):
                        with st.expander(f"🎬 Segment: {part.get('segment', 'Next Step')}"):
                            st.write(part.get("script_text"))
                            st.caption(f"💥 **Editing/SFX Cue:** {part.get('editing_cue')}")
                            
                    # 4. Outro
                    st.markdown("### 🔄 Smart End-Screen Outro")
                    st.info(result_json.get("outro_retention"))
                    
                except Exception as e:
                    st.error(f"Matrix glitch occurred: {e}")
