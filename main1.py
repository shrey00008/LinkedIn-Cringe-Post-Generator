import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("apikey")
client = Groq(api_key=apikey)


st.set_page_config(page_title="LinkedIn Cringe Generator", page_icon="👔", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    .linkedin-card {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        color: #000000 !important;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        text-align: left;
        margin-top: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }

    .post-header { display: flex; align-items: center; margin-bottom: 12px; }
    .profile-pic { width: 48px; height: 48px; background-color: #dee2e6; border-radius: 50%; margin-right: 12px; }
    .profile-info b { font-size: 14px; color: rgba(0,0,0,0.9); }
    .profile-info p { font-size: 12px; color: rgba(0,0,0,0.6); margin: 0; }

    .post-content { font-size: 14px; color: rgba(0,0,0,0.9); line-height: 1.5; }
    .linkedin-blue { color: #0a66c2; font-weight: 600; text-decoration: none; }

    .interaction-bar {
        border-top: 1px solid #f3f2ef;
        padding-top: 8px;
        margin-top: 12px;
        display: flex;
        justify-content: space-around;
        color: rgba(0,0,0,0.6);
        font-weight: 600;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

def generate(userInput):
    
    systemInstructions = (
        "You are a LinkedIn Viral growth Bot. Your job is to take a mundane user event "
        "and transform it into a high engagement 'Bro-etry' post. "
        "Rules: \n"
        "1. Every sentence must be punchy.\n"
        "2. Turn failures into pivotal leadership moments.\n"
        "3. You must only output a JSON object with these keys: "
        "4. 2-3 emojis are allowed in the whole post. "
        "5. May include sarcastic words. "
        "'hook', 'transformation_story', 'businesslesson', 'cringe_rating', 'hashtags'."
    )
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": systemInstructions},
            {"role": "user", "content": f"The event: {userInput}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)


st.title("👔 Viral LinkedIn Generator")
st.write("Convert your mundane reality into 'Thought Leadership' gold.")

userThought = st.text_area("What happened today?", placeholder="Ex: I forgot my laptop charger...", height=100)
generate_btn = st.button("Generate Alpha Content 🚀", use_container_width=True)

if generate_btn and userThought:
    with st.spinner("Extracting 'thought leadership'...."):
        try:
            data = generate(userThought)
            
            # --- YOUR ORIGINAL PRINT LOGIC ---
            # Splitting by period and stripping whitespace for vertical alignment
            sentences = [s.strip() for s in data['transformation_story'].split(".") if s.strip()]
            formatted_story = ".<br><br>".join(sentences) + "." if sentences else ""

            # Mapping your exact JSON keys to the HTML UI
            post_html = f"""
            <div class="linkedin-card">
                <div class="post-header">
                    <div class="profile-pic"></div>
                    <div class="profile-info">
                        <b>You (AI Optimized)</b><br>
                        <p>Thought Leader | Disrupting Reality | AI Strategist</p>
                        <p>1h • Edited • 🌐</p>
                    </div>
                </div>
                <div class="post-content">
                    <p><b>{data['hook']}</b></p>
                    <p>{formatted_story}</p>
                    <p><b>Lesson:</b> {data['businesslesson']}</p>
                    <p class="linkedin-blue">{' '.join(data['hashtags'])}</p>
                    <br>Agree??
                </div>
                <div class="interaction-bar">
                    <span>👍 Like</span>
                    <span>💬 Comment</span>
                    <span>🔁 Repost</span>
                    <span>📤 Send</span>
                </div>
            </div>
            """
            
            # THE GIMMICK: Analytics Table (Streamlit version)
            col1, col2 = st.columns(2)
            cringe_val = data.get('cringe_rating', '99')
            col1.metric("Cringe Rating", f"{cringe_val}%", delta="Maximum", delta_color="inverse")
            col2.metric("Status", "Alpha", delta="🚀")

            st.markdown(post_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Logic Error: {e}")
else:
    st.info("Input a thought to begin the transformation.")