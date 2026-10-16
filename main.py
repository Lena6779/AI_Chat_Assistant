import os
import time
import streamlit as st

st.set_page_config(page_title="AI Chat", page_icon="💬")
st.title("\U0001F4AC AI Chat Assistant")

# Chat history lives in session state so it survives every rerun
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# Sidebar 
CONTEXT_OPTIONS = {
    "Include Python expertise": "You are an expert Python developer. Give idiomatic, well-commented code examples.",
    "Include web development context": "You understand web development: HTML, CSS, JavaScript, REST APIs, and frameworks like FastAPI.",
    "Include AI/ML context": "You are knowledgeable about AI/ML: LLMs, prompt engineering, embeddings, and model evaluation.",
}

with st.sidebar:
    st.header(" ⚙️ Settings")
    
    base_prompt = st.text_area(
        "System prompt (AI personality)",
        value="You are a friendly, helpful assistant who explains things clearly.",
        height=120,
    )

    st.subheader("Context")
    selected_contexts = [label for label in CONTEXT_OPTIONS if st.checkbox(label)]

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
        
def build_system_prompt(base, selected):
    parts = [base.strip()]
    for label in selected:
        parts.append(CONTEXT_OPTIONS[label])
    return "\n\n".join(parts)

system_prompt = build_system_prompt(base_prompt, selected_contexts)

with st.sidebar.expander("Preview final system prompt"):
    st.write(system_prompt)
    
MOCK_TIPS = {
    "Include Python expertise": "From a Python angle, I'd suggest breaking this into small functions and testing each one.",
    "Include web development context": "From a web dev angle, think about how this would work as an API endpoint or on a page.",
    "Include AI/ML context": "From an AI/ML angle, consider what data you'd need and how you'd evaluate the results.",
}


def mock_response(user_message, base, selected):
    time.sleep(1.5)  # pretend to think so the spinner is visible
    lines = [
        f'You asked: "{user_message}"',
        f"**My personality:** {base.strip()}",
    ]
    if selected:
        lines.append("**Context I'm using:** " + ", ".join(selected))
        for label in selected:
            lines.append(MOCK_TIPS[label])
    else:
        lines.append("No extra context selected. Try checking a box in the sidebar!")
    lines.append("_(Mock mode: set an OPENAI_API_KEY environment variable for real answers.)_")
    return "\n\n".join(lines)


def real_response(system_prompt, messages, api_key):
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + messages,
    )
    return response.choices[0].message.content

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
if prompt := st.chat_input("Ask me anything..."):
    # 1. Save and show the user's message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and show the reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    reply = real_response(system_prompt, st.session_state.chat_history, api_key)
                except Exception as e:
                    reply = f"API error: {e}\n\n" + mock_response(prompt, base_prompt, selected_contexts)
            else:
                reply = mock_response(prompt, base_prompt, selected_contexts)
        st.markdown(reply)

    # 3. Save the reply so it shows up after the next rerun
    st.session_state.chat_history.append({"role": "assistant", "content": reply})