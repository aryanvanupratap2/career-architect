import streamlit as st
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BASE_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="Career AI Architect",
    page_icon="🗺️",
    layout="wide"
)
# Styling
st.markdown("""
    <style>
    /* Main container for the vertical flow */
    .roadmap-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
        font-family: 'Inter', sans-serif;
    }
    
    /* The interactive nodes */
    .roadmap-node {
        background-color: #ffffff;
        border: 2px solid #007bff;
        border-radius: 12px;
        padding: 20px;
        width: 90%;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,123,255,0.1);
        margin-bottom: 0px;
        transition: all 0.3s ease;
    }
    
    .roadmap-node:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,123,255,0.2);
        border-color: #0056b3;
    }
    
    /* The connecting lines */
    .connector {
        width: 4px;
        height: 40px;
        background: linear-gradient(to bottom, #007bff, #00d4ff);
    }
    
    .node-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #111;
        margin-bottom: 5px;
    }

    /* Styling for the expander inside the columns */
    .stExpander {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper Functions
def api_request(method, endpoint, data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        # Return both the json and status code for error handling
        return response.json(), response.status_code
    except Exception as e:
        return {"detail": str(e)}, 500

# Initialize Session State
if "token" not in st.session_state:
    st.session_state.token = None
if "roadmap_result" not in st.session_state:
    st.session_state.roadmap_result = None

# Sidebar: Authentication
with st.sidebar:
    st.title("🛡️ Auth Portal")
    
    if st.session_state.token:
        st.success("You are logged in!")
        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.roadmap_result = None
            st.rerun()
    else:
        auth_mode = st.tabs(["Login", "Register"])
        
        with auth_mode[0]:
            l_email = st.text_input("Email", key="l_email")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Sign In", use_container_width=True):
                # Using LoginRequest schema
                res, code = api_request("POST", "/auth/login", {"email": l_email, "password": l_pass})
                if code == 200:
                    st.session_state.token = res["access_token"]
                    st.rerun()
                else:
                    st.error(res.get("detail", "Login Failed"))

        with auth_mode[1]:
            r_name = st.text_input("Name")
            r_email = st.text_input("Email", key="r_email")
            r_pass = st.text_input("Password", type="password", key="r_pass")
            r_qual = st.text_input("Qualification")
            r_aim = st.text_input("Aim")
            if st.button("Create Account", use_container_width=True):
                # Using RegisterRequest schema
                payload = {
                    "name": r_name, "email": r_email, "password": r_pass,
                    "qualification": r_qual, "aim": r_aim
                }
                res, code = api_request("POST", "/auth/register", payload)
                if code == 200:
                    st.success("Account Created! Please Login.")
                else:
                    st.error(res.get("detail", "Registration Failed"))

# Main interface
if not st.session_state.token:
    st.title("🚀 Career Path Architect")
    st.info("Unlock your personalized 6-month career roadmap by logging in.")
    st.image("https://roadmap.sh/images/og-main.png", caption="Inspired by roadmap.sh") # Optional visual flavor

else:
    st.title("🗺️ Your Interactive Career Roadmap")
    
    col_input, col_viz = st.columns([1, 2], gap="large")

    with col_input:
        st.subheader("⚙️ Path Parameters")
        with st.container(border=True):
            current_qual = st.text_input("Your Qualification", placeholder="e.g. B.Tech CS")
            target_aim = st.text_input("Your Career Goal", placeholder="e.g. DevOps Engineer")
            skills = st.text_area("Current Skillset", placeholder="Python, Docker, Linux...")

            if st.button("Generate My Roadmap ✨", use_container_width=True):
                with st.spinner("AI is analyzing market trends..."):
                    payload = {
                        "qualification": current_qual,
                        "skills": skills,
                        "aim": target_aim
                    }
                    # Calls the LangGraph flow
                    res, code = api_request("POST", "/career/generate", payload, st.session_state.token)
                    
                    if code == 200:
                        # Extracting the string from the dict response
                        if isinstance(res, dict) and "roadmap" in res:
                            st.session_state.roadmap_result = res["roadmap"]
                        else:
                            st.session_state.roadmap_result = res
                    else:
                        st.error(f"Error: {res.get('detail')}")

    with col_viz:
        if st.session_state.roadmap_result:
            st.subheader("📍 Journey Milestones")
            
            # Parsing the Gemini output
            raw_text = st.session_state.roadmap_result
            # Split by markdown H3 headers
            stages = re.split(r'### ', str(raw_text))
            
            st.markdown('<div class="roadmap-container">', unsafe_allow_html=True)
            
            for idx, stage in enumerate(stages):
                if not stage.strip(): continue
                
                # Logic to separate title from the resources/links
                parts = stage.strip().split('\n', 1)
                title = parts[0]
                content = parts[1] if len(parts) > 1 else ""

                # Render Visual Node
                st.markdown(f"""
                    <div class="roadmap-node">
                        <div class="node-title">{title}</div>
                    </div>
                """, unsafe_allow_html=True)

                # Render Content/Links in an expander for clean UI
                with st.expander(f"📖 Explore {title}"):
                    st.markdown(content)

                # Add connecting line
                if idx < len(stages) - 1:
                    st.markdown('<div class="connector"></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:

            st.info("Provide your details and click 'Generate' to see your step-by-step guide.")

