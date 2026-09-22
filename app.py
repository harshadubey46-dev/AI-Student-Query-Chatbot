import streamlit as st
from chatbot import get_response


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Student Query Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ---------- Background ---------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #fff8fc 0%,
            #f8f6ff 50%,
            #f2f9ff 100%
        );
    }

    .main {
        padding-top: 0.8rem;
        padding-bottom: 1rem;
    }


    /* ---------- Main title ---------- */

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #353147;
        margin-bottom: 4px;
    }

    .main-subtitle {
        text-align: center;
        font-size: 16px;
        color: #777286;
        margin-bottom: 12px;
    }


    /* ---------- Status ---------- */

    .status-box {
        text-align: center;
        margin-bottom: 25px;
    }

    .status {
        display: inline-block;
        background: #e9f8ee;
        color: #27834b;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }


    /* ---------- Welcome box ---------- */

    .welcome-box {
        background: rgba(255, 255, 255, 0.90);
        border: 1px solid #e5e0ef;
        border-radius: 18px;
        padding: 15px 20px;
        margin-bottom: 18px;
        box-shadow: 0 5px 18px rgba(70, 55, 100, 0.06);
    }

    .welcome-title {
        font-size: 19px;
        font-weight: 700;
        color: #403a54;
        margin-bottom: 7px;
    }

    .welcome-text {
        font-size: 14px;
        color: #706b7d;
        line-height: 1.6;
    }


    /* ---------- Section headings ---------- */

    .section-title {
        font-size: 20px;
        font-weight: 750;
        color: #403a54;
        margin-top: 20px;
        margin-bottom: 12px;
    }


    /* ---------- Quick question buttons ---------- */

    div.stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 12px;
        border: 1px solid #dfdbea;
        background: rgba(255, 255, 255, 0.90);
        color: #484258;
        font-size: 14px;
        font-weight: 600;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        border-color: #b8a6e6;
        color: #6951a7;
        background: #fbf9ff;
    }


    /* ---------- Chat messages ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 15px;
        margin-bottom: 8px;
    }

    [data-testid="stChatMessage"] p {
        font-size: 15px;
        line-height: 1.55;
    }


    /* ---------- Chat input ---------- */

    [data-testid="stChatInput"] {
        margin-top: 15px;
    }


    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #8b8698;
        font-size: 12px;
        margin-top: 18px;
        padding-bottom: 5px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<div class='main-title'>🤖 AI Student Query Chatbot</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='main-subtitle'>"
    "Your friendly virtual assistant for common student queries"
    "</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='status-box'>"
    "<span class='status'>🟢 Online • Ready to help</span>"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# CHAT INITIALIZATION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# WELCOME MESSAGE
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        "<div class='welcome-box'>"
        "<div class='welcome-title'>"
        "👋 Hello! Welcome to the Student Help Desk"
        "</div>"
        "<div class='welcome-text'>"
        "Ask me about courses, fees, admission, examinations, "
        "timings, attendance, scholarships, or college contact "
        "information. You can type your question below or choose "
        "a quick question."
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# =========================================================
# QUICK QUESTIONS
# =========================================================

st.markdown(
    "<div class='section-title'>✨ Quick Questions</div>",
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    courses_button = st.button(
        "🎓 Courses",
        key="courses_button"
    )

    fees_button = st.button(
        "💰 Fees",
        key="fees_button"
    )

    attendance_button = st.button(
        "📊 Attendance",
        key="attendance_button"
    )


with col2:

    admission_button = st.button(
        "📝 Admission",
        key="admission_button"
    )

    exams_button = st.button(
        "📚 Exams",
        key="exams_button"
    )

    contact_button = st.button(
        "📞 Contact",
        key="contact_button"
    )


with col3:

    timings_button = st.button(
        "🕐 Timings",
        key="timings_button"
    )

    scholarship_button = st.button(
        "🎓 Scholarship",
        key="scholarship_button"
    )

    help_button = st.button(
        "💡 Help",
        key="help_button"
    )


# =========================================================
# BUTTON QUESTIONS
# =========================================================

suggested_question = None


if courses_button:
    suggested_question = "What courses are available?"

elif fees_button:
    suggested_question = "What are the fees?"

elif attendance_button:
    suggested_question = "What is the attendance requirement?"

elif admission_button:
    suggested_question = "How can I get admission?"

elif exams_button:
    suggested_question = "When are the exams?"

elif contact_button:
    suggested_question = "How can I contact the college?"

elif timings_button:
    suggested_question = "What are the college timings?"

elif scholarship_button:
    suggested_question = "Are scholarships available?"

elif help_button:
    suggested_question = "What can you help me with?"


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "💬 Type your question here..."
)


if suggested_question:

    user_input = suggested_question


# =========================================================
# PROCESS QUESTION
# =========================================================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = get_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()


# =========================================================
# CLEAR CHAT
# =========================================================

st.divider()

left, center, right = st.columns([1, 2, 1])

with center:

    if st.button(
        "🗑️ Clear Conversation",
        key="clear_conversation"
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    "<div class='footer'>"
    "AI Student Query Chatbot • NLP & Pattern Matching"
    "</div>",
    unsafe_allow_html=True
)