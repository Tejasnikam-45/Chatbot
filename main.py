import streamlit as st
import backend
import time
import database

# Routing control
if "page" not in st.session_state:
    st.session_state.page = "login"

# Logout logic
def logout():
    st.session_state.page = "login"
    st.session_state.pop("username", None)
    st.session_state.pop("messages", None)

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #0f172a;
        }
        .title-style {
            font-size: 36px;
            font-weight: bold;
            color: #FFEA00;
            margin-bottom: 20px;
        }
        .input-style label {
            font-weight: bold;
            color: #FFFFFF;
        }
        .stTextInput > div > div > input {
            background-color: #1e293b;
            color: white;
        }
        .stTextInput label {
            color: white;
        }
        .stButton > button {
            background-color: #10b981;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            margin-top: 10px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #059669;
        }
        .link {
            font-size: 14px;
            color: #61dafb;
            text-decoration: underline;
        }
        .logout-button {
            display: flex;
            justify-content: flex-end;
            margin-top: -50px;
            margin-bottom: 10px;
        }
        .logout-button button {
            background-color: #ef4444;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Signup Page
def signup():
    st.markdown("<div class='title-style'>🔐 Signup for ACPCE Chatbot</div>", unsafe_allow_html=True)
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")

    if st.button("Create Account"):
        if database.add_user(username, password):
            st.success("Account created successfully!")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Username already exists!")

    st.markdown("<span class='link'>Already have an account?</span>", unsafe_allow_html=True)
    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()

# Login Page
def login():
    st.markdown("<div class='title-style'>🔒 Login to ACPCE Chatbot</div>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if database.verify_user(username, password):
            st.success("Login successful! 🚀")
            st.session_state.username = username
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")

    st.markdown("<span class='link'>Don't have an account?</span>", unsafe_allow_html=True)
    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()

# Chat Page
def chat():
    st.markdown(f"<div class='title-style'>💬 Welcome, {st.session_state.username}!</div>", unsafe_allow_html=True)

    # Logout button at the top-right
    st.markdown('<div class="logout-button">', unsafe_allow_html=True)
    if st.button("Logout"):
        logout()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    def response_generator(prompt):
        response = backend.GenerateResponse(prompt)
        for word in response.split():
            yield word + " "
            time.sleep(0.03)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything! 💬"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})

# Page Controller
if st.session_state.page == "login":
    login()
elif st.session_state.page == "signup":
    signup()
elif st.session_state.page == "chat":
    chat()
