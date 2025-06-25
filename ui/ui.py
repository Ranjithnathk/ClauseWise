import streamlit as st
import requests
import html
import os

st.set_page_config(page_title="ClauseWise ⚖️", layout="wide")
#API_URL = "http://127.0.0.1:8000"
API_URL = "https://clausewise-backend-140738413424.us-central1.run.app"

# --- Custom Styles ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        height: 100vh;
        overflow: hidden;
    }

    .stHorizontalBlock > div:first-child {
        background-color: #E4EFE7;
        padding: 1rem;
        border-radius: 10px;
        max-height: 80vh;
        overflow-y: auto;
        box-sizing: border-box;
    }

    .stHorizontalBlock > div:nth-child(2) {
        background-color: #ffffff;
        padding: 0;
        border-radius: 10px;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .chat-header {
        flex: 0 0 0%;
    }

    .scrollable-chat-box {
        flex: 0 0 100%;
        overflow-y: auto;
        padding: 0;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #fefefe;
        margin: 0 0;
        box-sizing: border-box;
        aspect-ratio: 7 / 3;
    }

    .chat-input {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 8px;
    }

    .chat-input textarea {
        flex-grow: 1;
        height: 80px !important;
        resize: none;
    }

    .chat-input button {
        flex-shrink: 0;
        width: 40px;
        height: 40px;
        font-size: 22px;
        cursor: pointer;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0;
        margin: 0;
    }

    .user-msg {
        background-color: #dcf8c6;
        padding: 10px 14px;
        border-radius: 16px;
        margin: 6px 0;
        max-width: 50%;
        margin-left: auto;
        text-align: right;
    }

    .ai-msg {
        background-color: #f1f1f1;
        padding: 10px 14px;
        border-radius: 16px;
        margin: 6px 0;
        max-width: 70%;
        margin-right: auto;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# --- Init session state ---
for key, default in {
    "token": None, "username": None, "chat_history": [],
    "last_model": None, "last_pdf": None, "show_signup": False,
    "pdfs": [], "clear_input": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Auth Functions ---
def logout():
    for key in [
        "token", "username", "chat_history",
        "last_model", "last_pdf", "show_signup", "pdfs"
    ]:
        st.session_state[key] = None if key != "chat_history" else []
    st.rerun()

def get_pdfs():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/available_pdfs", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                "public": data.get("public", []),
                "user": data.get("user", [])
            }
        else:
            return {"public": [], "user": []}
    except Exception:
        return {"public": [], "user": []}

def upload_user_pdf(file):
    if not file:
        st.warning("Please upload a valid PDF.")
        return
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }
        files = {
            "file": (file.name, file, "application/pdf")
        }
        response = requests.post(f"{API_URL}/upload_pdf", files=files, headers=headers)
        if response.status_code == 200:
            st.success("PDF uploaded and indexed successfully!")
            st.session_state.pdfs = get_pdfs()
            st.rerun()
        else:
            st.error("Upload failed: " + response.text)
    except Exception as e:
        st.error(f"Upload error: {e}")

# --- Main Chat UI ---
def main_ui():
    st.title("ClauseWise ⚖️")
    left_col, right_col = st.columns([3, 8], gap="small")

    with left_col:
        st.markdown(f"#### Welcome, **{st.session_state.username}**!")

        st.markdown("###### Select PDF")
        pdfs = st.session_state.pdfs or get_pdfs()
        
        # Combine public + user PDFs into one list, removing duplicates if any
        combined_pdfs = list(dict.fromkeys(pdfs.get("public", []) + pdfs.get("user", [])))

        if combined_pdfs:
            selected_pdf = st.selectbox("", combined_pdfs, key="selected_pdf", label_visibility="collapsed")
        else:
            st.warning("No PDFs found in the server.")
            selected_pdf = None

        # Update session state and reset chat if pdf changed
        if selected_pdf != st.session_state.last_pdf:
            st.session_state.chat_history = []
            st.session_state.last_pdf = selected_pdf
            st.session_state.clear_input = True

        # Upload PDF uploader (same as before)
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("Upload & Process PDF"):
                upload_user_pdf(uploaded_file)
                st.session_state.pdfs = get_pdfs()
                st.rerun()

        st.markdown("###### Select LLM Model")
        models = ["gpt-4o", "gemini-2.0-flash", "llama3-70b-8192", "mistral-saba-24b", "deepseek-r1-distill-llama-70b"]
        selected_model = st.selectbox("", models, label_visibility="collapsed")

        if st.button("Logout"):
            logout()

        if selected_model != st.session_state.last_model:
            st.session_state.chat_history = []
            st.session_state.last_model = selected_model
            st.session_state.clear_input = True

    with right_col:
        chat_html = '<div class="scrollable-chat-box">'
        for i in range(0, len(st.session_state.chat_history), 2):
            user_msg = html.escape(st.session_state.chat_history[i])
            ai_msg = html.escape(st.session_state.chat_history[i + 1]) if i + 1 < len(st.session_state.chat_history) else ""
            chat_html += f'<div class="user-msg">{user_msg}</div>'
            chat_html += f'<div class="ai-msg">{ai_msg}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        st.markdown(f"###### You are chatting with **{selected_model}** on **{selected_pdf}**")

        with st.container():
            st.markdown('<div class="chat-input">', unsafe_allow_html=True)
            input_value = "" if st.session_state.clear_input else st.session_state.get("input_box", "")
            user_input = st.text_area(
                "Your Message",
                height=80,
                key="input_box",
                label_visibility="collapsed",
                value=input_value,
                placeholder="Try asking for summaries, key points, or detailed explanations..."
            )
            st.session_state.clear_input = False  # Reset after render
            send_clicked = st.button("Send", key="send_button", help="Send", args=(), kwargs={}, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

        if send_clicked:
            prompt = user_input.strip()
            if prompt:
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    payload = {
                        "model_name": selected_model,
                        "pdf_name": selected_pdf,
                        "messages": st.session_state.chat_history + [prompt]
                    }
                    res = requests.post(f"{API_URL}/chat", json=payload, headers=headers)
                    answer = res.json().get("answer", "No answer received.")
                except Exception as e:
                    answer = f"Failed to connect to backend: {e}"

                st.session_state.chat_history.append(prompt)
                st.session_state.chat_history.append(answer)
                st.session_state.clear_input = True
                st.rerun()

# --- Auth Routing ---
def login():
    st.title("ClauseWise ⚖️")
    st.markdown("#### Your AI Attorney to clear your Legal doubts")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not username or not password:
            st.warning("Please enter both username and password.")
            return
        try:
            response = requests.post(f"{API_URL}/login", data={"username": username, "password": password}, headers={"Content-Type": "application/x-www-form-urlencoded"})
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state.token = token
                st.session_state.username = username
                st.session_state.pdfs = get_pdfs()
                st.success(f"Welcome back, {username}!")
                #st.code(token, language="bash")
                #st.stop()
                st.rerun()
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Login failed: {e}")

    if st.button("Create new account"):
        st.session_state.show_signup = True
        st.rerun()

def signup():
    st.title("ClauseWise ⚖️")
    st.markdown("#### Create a new account")
    username = st.text_input("Choose a username")
    email = st.text_input("Email")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Sign Up"):
        if not username or not email or not password or not confirm_password:
            st.warning("Please fill out all fields.")
            return
        if password != confirm_password:
            st.warning("Passwords do not match.")
            return
        try:
            response = requests.post(f"{API_URL}/signup", json={"username": username, "email": email, "password": password})
            if response.status_code in [200, 201]:
                st.success("Account created successfully! Please log in.")
                st.session_state.show_signup = False
                st.rerun()
            else:
                st.error(f"Signup failed: {response.json().get('detail', '')}")
        except Exception as e:
            st.error(f"Signup failed: {e}")

    if st.button("Already have an account?"):
        st.session_state.show_signup = False
        st.rerun()

# --- App Launch ---
if st.session_state.token is None:
    if st.session_state.show_signup:
        signup()
    else:
        login()
else:
    main_ui()
