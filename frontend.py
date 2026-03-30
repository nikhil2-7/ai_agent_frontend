import streamlit as st
import requests


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "https://ai-agent-backend-o0q4.onrender.com/chat"
HISTORY_URL = "https://ai-agent-backend-o0q4.onrender.com/history"

#for backend awake
import threading

def wake_backend():
    try:
        requests.get("https://ai-agent-backend-o0q4.onrender.com/")
    except:
        pass

if "backend_awake" not in st.session_state:
    threading.Thread(target=wake_backend).start()
    st.session_state.backend_awake = True
    #end
#for backend awake 
import time

def call_api(payload):
    for attempt in range(5):
        try:
            response = call_api(payload)
            #response = requests.post(API_URL, json=payload, timeout=30)

            if response.status_code == 200:
                return response

        except:
            pass

        time.sleep(5)

    return None
#end

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_chat_index" not in st.session_state:
    st.session_state.selected_chat_index = None

if "history_cache" not in st.session_state:
    try:
        st.session_state.history_cache = requests.get(HISTORY_URL).json()
    except:
        st.session_state.history_cache = []

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("## ⚙️ AI Configuration")

    provider = st.selectbox("Extensions / Provider", ["Groq"])

    MODEL_MAP = {
        "Groq": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
    }

    model = st.selectbox("Model Name", MODEL_MAP[provider])

    st.markdown("**Model**")
    st.caption(f"`{model}`")

    web_search = st.checkbox("🌐 Enable Web Search", value=False)

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant.",
        height=90,
    )

    st.divider()

    # ── COLLAPSIBLE HISTORY ─────────────────────────
    with st.expander("📋 History", expanded=False):

        history_data = st.session_state.history_cache

        if history_data:
            for i, chat in enumerate(history_data):

                if i == st.session_state.selected_chat_index:
                    label = f"👉 {chat['human'][:40]}"
                else:
                    label = f"💬 {chat['human'][:40]}"

                if st.button(label, key=f"history_{i}"):

                    st.session_state.selected_chat_index = i

                    st.session_state.messages = [
                        {"role": "user", "text": chat["human"]},
                        {"role": "ai", "text": chat["ai"]}
                    ]
        else:
            st.caption("No previous conversations.")

    if st.button("Clear Screen ", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_chat_index = None

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🤖 AI Assistant")
st.caption("⚡ First response may take 15–30 seconds due to server cold start.")
st.caption(
    "Powered by " + provider + " · " + model +
    ("  🌐 Web Search ON" if web_search else "")
)

st.markdown(
    '<div style="background:#2d1f07;border:1px solid #d97706;border-radius:10px;padding:10px 14px;font-size:13px;color:#fcd34d;margin-bottom:16px;">'
    '⚠️ <b>AI Disclaimer:</b> Responses are AI-generated and may be inaccurate. '
    'Always verify important information independently.</div>',
    unsafe_allow_html=True,
)

# ── Chat display ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**👤 You:** {msg['text']}")
    else:
        st.markdown(f"**🤖 AI:** {msg['text']}")

st.markdown("---")

# new change for automatic call api
# def call_api(payload):
#     for attempt in range(3):  # retry 3 times
#         try:
#             response = requests.post(API_URL, json=payload, timeout=30)

#             if response.status_code == 200:
#                 return response

#         except requests.exceptions.RequestException:
#             time.sleep(5)  # wait before retry

#     return None
#new change automatically send by enter press


# # ── Text Input ────────────────────────────────────────────────────────────────
# user_input = st.text_area("type your message...")
# #     "Your message",
# #     placeholder="Type your message here…",
# #     height=80,
# #     label_visibility="collapsed",
# # )

# # col1, col2 = st.columns([5, 1])

# # with col1:
# #     send = st.button("📨 Send", use_container_width=True)



# # ── Handle Send ───────────────────────────────────────────────────────────────
# if user_input:

#     user_message = user_input.strip()

#     if user_message:

#         st.session_state.selected_chat_index = None

#         st.session_state.messages.append({
#             "role": "user",
#             "text": user_message
#         })

#         payload = {
#             "model_name": model,
#             "model_provider": provider,
#             "system_prompt": system_prompt,
#             "messages": [user_message],
#             "allow_search": web_search
#         }

#         try:
#             with st.spinner("Thinking..."):
#                 response = requests.post(API_URL, json=payload)
#                 #response = call_api(payload)

#             if response and response.status_code == 200:

#                 data = response.json()

#                 if data.get("type") == "text":
#                     ai_reply = data.get("content", "")

#                 elif data.get("type") == "image":
#                     st.session_state.messages.append({
#                         "role": "ai",
#                         "text": "🖼 Image Generated Below:"
#                     })
#                     st.image(data.get("content"))
#                     st.rerun()

#                 else:
#                     ai_reply = str(data)

#             else:
#                 ai_reply = "⚠️ Backend is waking up... please try again in a few seconds."#"⚠️ Backend error"

#         except Exception as e:
#             ai_reply = f"❌ Connection error: {str(e)}"

#         st.session_state.messages.append({
#             "role": "ai",
#             "text": ai_reply
#         })
#         # Refresh history from backend
#         try:
#             st.session_state.history_cache = requests.get(HISTORY_URL).json()
#         except:
#             pass

#         st.rerun()


#for bakend awake
# ── Chat Input (FIXED) ────────────────────────────────────────
user_input = st.chat_input("Type your message...")

if user_input:
    user_message = user_input.strip()

    st.session_state.selected_chat_index = None

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "text": user_message
    })

    payload = {
        "model_name": model,
        "model_provider": provider,
        "system_prompt": system_prompt,
        "messages": [user_message],
        "allow_search": web_search
    }

    try:
        with st.spinner("Thinking..."):
            response = call_api(payload)   # ✅ use retry function

        if response and response.status_code == 200:
            data = response.json()

            if data.get("type") == "text":
                ai_reply = data.get("content", "")

            elif data.get("type") == "image":
                st.session_state.messages.append({
                    "role": "ai",
                    "text": "🖼 Image Generated Below:"
                })
                st.image(data.get("content"))
                st.rerun()

            else:
                ai_reply = str(data)

        else:
            ai_reply = "⏳ Backend starting... please wait a few seconds."

    except Exception as e:
        ai_reply = f"❌ Connection error: {str(e)}"

    # Add AI response
    st.session_state.messages.append({
        "role": "ai",
        "text": ai_reply
    })

    # Refresh history
    try:
        st.session_state.history_cache = requests.get(HISTORY_URL).json()
    except:
        pass

    st.rerun()