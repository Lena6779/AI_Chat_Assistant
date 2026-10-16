# 💬 AI Chat Assistant

A Streamlit chat app with a customizable AI personality. You can edit the system prompt, add expert context with checkboxes, and chat with either a real OpenAI model or a built-in mock.

## Features

- **Chat interface** built with `st.chat_message()` and `st.chat_input()`
- **Persistent chat history** stored in `st.session_state` and re-rendered on every run
- **Sidebar settings:**
  - Editable system prompt to set the AI's personality
  - Context checkboxes that add expertise to the system prompt:
    - Python expertise
    - Web development context
    - AI/ML context
  - Preview of the final system prompt
  - **Clear Chat** button to reset the conversation
- **Loading indicator** with `st.spinner("Thinking...")` while a reply is generated
- **Two response modes:**
  - **Real mode:** uses the OpenAI API when an `OPENAI_API_KEY` is set
  - **Mock mode:** used when no key is set; the reply echoes your message, the system prompt, and the selected contexts

## Tech Stack

- Python 3
- [Streamlit](https://streamlit.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python) (optional, for real responses)

## Setup

1. **Clone the repo and open the folder:**

   ```bash
   git clone <your-repo-url>
   cd AI_Assistant
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   ```

   - Windows (PowerShell): `venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`

3. **Install the packages:**

   ```bash
   pip install streamlit openai
   ```

## Running the App

```bash
streamlit run main.py
```

The app opens in your browser at `http://localhost:8501`.

> **Note:** Start the app with `streamlit run`, not `python main.py`. Running it with plain Python won't open the app.

## Using a Real AI Model (Optional)

Without an API key, the app runs in mock mode. To get real answers, set your OpenAI key before starting the app:

- Windows (PowerShell): `$env:OPENAI_API_KEY="sk-..."`
- Mac/Linux: `export OPENAI_API_KEY="sk-..."`

Never commit your API key. The `.gitignore` excludes `.env` and `.streamlit/secrets.toml`.

## How It Works

1. Your message is added to `st.session_state.chat_history` and displayed.
2. The system prompt is built from the sidebar text area plus the text for each checked context.
3. While "Thinking..." shows, the app either:
   - sends the system prompt and full chat history to OpenAI, or
   - creates a mock reply if no key is set (or the API call fails).
4. The reply is displayed and saved to the chat history so it stays on screen after each rerun.

## Project Structure

```
AI_Assistant/
├── main.py         # Streamlit chat app
├── README.md
└── .gitignore
```

## Author

Lena Hersloff, Coding Temple AI Engineering Foundations