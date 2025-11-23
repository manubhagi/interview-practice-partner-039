# 🤖 Interview Practice Partner

An AI-powered mock interview agent designed to help candidates practice for various roles. The agent conducts realistic voice/chat interviews, adapts to the user's behavior, and provides structured feedback at the end.

## 🚀 Features

-   **Role-Specific Interviews**: Supports profiles like Software Engineer, Product Manager, Sales, etc.
-   **Intelligent Follow-ups**: Doesn't just ask a list of questions; listens to your answers and probes deeper.
-   **Adaptive Personas**:
    -   *Confused User?* The agent guides and simplifies.
    -   *Efficient User?* The agent speeds up.
    -   *Chatty User?* The agent politely steers back to the topic.
-   **Structured Feedback**: Provides a detailed report on Strengths, Weaknesses, and Scores (Communication & Technical) after the session.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI
-   **Frontend**: Streamlit
-   **AI Model**: Google Gemini 1.5 Flash (via API)
-   **State Management**: In-memory session store

## 🏗️ Architecture

The system follows a client-server architecture:

1.  **Frontend (Streamlit)**:
    -   Captures user input.
    -   Maintains the chat history UI.
    -   Communicates with the backend via REST API.
2.  **Backend (FastAPI)**:
    -   `POST /start_session`: Initializes the interview context (System Prompt).
    -   `POST /chat`:
        -   Retrieves session history.
        -   Constructs a dynamic prompt for the LLM.
        -   Decides whether to ask a follow-up or a new question.
    -   `POST /feedback`: Sends the full transcript to the LLM for analysis.
3.  **LLM Layer (Gemini)**:
    -   Acts as the "Brain".
    -   Uses specific System Prompts to enforce the interviewer persona.

## 🏃‍♂️ How to Run Locally

### Prerequisites
-   Python 3.9+
-   A Google Gemini API Key (Free)

### Steps

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd interview-practice-partner
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables**
    -   Create a `.env` file in the root directory.
    -   Add your API key:
        ```env
        GEMINI_API_KEY=your_api_key_here
        ```

4.  **Start the Backend**
    ```bash
    uvicorn backend.main:app --reload
    ```

5.  **Start the Frontend** (in a new terminal)
    ```bash
    streamlit run frontend/app.py
    ```

6.  **Open Browser**
    -   Go to `http://localhost:8501` to start practicing!

## 🧠 Design Decisions

-   **FastAPI vs Flask**: Chosen FastAPI for better performance (async) and automatic data validation (Pydantic), which is crucial for structured LLM outputs.
-   **Streamlit**: Chosen for rapid prototyping. It allows building a chat interface in minutes, letting us focus on the *AI logic* rather than CSS/JS.
-   **Prompt Engineering**: Instead of complex state machines, we use "Persona Prompts". The System Prompt instructs the LLM to detect if a user is "Confused" or "Efficient" and adapt its tone dynamically. This makes the agent feel more "human" and less robotic.

## 🔮 Future Improvements

-   **Voice Mode**: Add Speech-to-Text (Whisper) and Text-to-Speech (ElevenLabs) for a full voice interview experience.
-   **Database**: Move from in-memory to PostgreSQL to save user progress.
-   **Resume Parsing**: Allow users to upload a PDF resume for tailored questions.
