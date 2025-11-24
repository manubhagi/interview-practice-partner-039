# 🤖 AI Interview Practice Partner

An intelligent AI-powered mock interview system that conducts realistic, adaptive interviews with voice and text support. Built with Google Gemini AI, this application helps candidates practice for various roles with natural conversation flow and detailed feedback.

---

## ✨ Key Features

### 🎯 **Core Capabilities**
- **18+ Role-Specific Interviews**: Software Engineer, Data Scientist, Product Manager, UX Designer, and more
- **Voice + Text Hybrid Interface**: Speak naturally for behavioral questions, type for code/SQL
- **Intelligent Conversation Flow**: AI adapts to your answers, asks follow-ups, and probes for depth
- **Structured Feedback**: Detailed performance analysis with strengths, improvements, and hiring verdict
- **Resume-Aware Questions**: Upload your resume for personalized, experience-based questions

### 🎙️ **Advanced Voice Features**
- **Unlimited Speech Duration**: Auto-restart technology bypasses browser's 60-second limit
- **15-Second Silence Detection**: Automatically stops recording after pauses
- **Real-Time Transcript**: See your speech as you talk (optional)
- **Interview Timer**: Track elapsed time during the session

### 🧠 **Smart AI Behavior**
- **Adaptive Personas**: Detects if you're confused, efficient, or chatty and adjusts accordingly
- **Technical Question Intelligence**: Only asks for typed answers when necessary (code, SQL, formulas)
- **Natural Follow-ups**: Doesn't just run through a list - actually listens and responds
- **Role-Appropriate Questions**: Software roles get coding problems, PM roles get product scenarios

### 🔑 **API Key Management**
- **Automatic Key Rotation**: Add multiple API keys for extended usage (600+ requests/day with 3 keys)
- **Smart Failover**: Automatically switches to next key when rate limit is hit
- **Seamless Experience**: Users never notice the key switching

---

## 🏗️ Architecture

### **System Design**

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  Voice Input   │  │  Text Input  │  │  Chat Display   │ │
│  │  (Web Speech)  │  │  (Textarea)  │  │  (Conversation) │ │
│  └────────────────┘  └──────────────┘  └─────────────────┘ │
│           │                  │                   │           │
│           └──────────────────┴───────────────────┘           │
│                              │                               │
│                         Fetch API                            │
└──────────────────────────────┼───────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                           │  │
│  │  • POST /start_session  → Initialize interview       │  │
│  │  • POST /chat           → Process user responses     │  │
│  │  • POST /feedback       → Generate final feedback    │  │
│  │  • POST /upload_resume  → Parse resume (optional)    │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Session Management (In-Memory Store)                │  │
│  │  • Conversation history                              │  │
│  │  • Question tracking                                 │  │
│  │  • Role/experience context                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│                              ▼                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LLM Client (Multi-Key Support)                      │  │
│  │  • Automatic key rotation                            │  │
│  │  • Rate limit detection                              │  │
│  │  • Failover handling                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────┼───────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Google Gemini API   │
                    │  (gemini-2.0-flash)  │
                    └──────────────────────┘
```

### **Data Flow**

1. **Session Start**: User selects role/experience → Backend creates session with system prompt
2. **Interview Loop**: 
   - User speaks/types → Frontend sends to `/chat`
   - Backend analyzes answer quality → Decides follow-up or next question
   - AI response → Text-to-Speech → User hears question
3. **Feedback**: After N questions → `/feedback` generates structured analysis

---

## 🚀 Setup Instructions

### **Prerequisites**
- Python 3.9+
- Google Gemini API Key(s) - [Get one free](https://aistudio.google.com/app/apikey)
- Modern browser (Chrome/Edge recommended for voice features)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd interview-practice-partner-039
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   
   Create a `.env` file in the root directory:
   ```env
   # Primary key (required)
   GEMINI_API_KEY=your_first_api_key_here
   
   # Additional keys for extended usage (optional)
   GEMINI_API_KEY_2=your_second_api_key_here
   GEMINI_API_KEY_3=your_third_api_key_here
   ```
   
   **Important**: Each key should be from a **different Google Cloud project** to get separate quotas.

4. **Start the backend**
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Open the application**
   
   Navigate to: `http://localhost:8000/app/`

6. **Start practicing!** 🎉

---

## 🎯 Usage Guide

### **Starting an Interview**
1. Select your target role (e.g., Software Engineer)
2. Choose experience level (Junior/Mid/Senior)
3. (Optional) Upload your resume for personalized questions
4. Click "Start Interview"

### **During the Interview**
- **For behavioral questions**: Speak naturally into your microphone
- **For coding/SQL questions**: Type your answer in the left text box
- **Manual stop**: Click "Done Speaking" to stop recording early
- **Auto-stop**: Recording stops after 15 seconds of silence

### **Getting Feedback**
- Click "End Interview & Get Feedback" when ready
- Review your structured performance analysis
- Note areas for improvement and next steps

---

## 🧠 Design Decisions

### **1. Voice + Text Hybrid Approach**
**Why?** 
- Behavioral questions benefit from natural speech
- Code/SQL requires precise formatting
- Hybrid approach gives best of both worlds

**Implementation:**
- Web Speech API for voice recognition
- Auto-restart mechanism for unlimited speech duration
- Smart detection of when to request typed answers

### **2. Auto-Restart Voice Recognition**
**Problem:** Browser's Web Speech API stops after ~60 seconds

**Solution:** 
- Accumulate transcript across multiple recording sessions
- Automatically restart recognition when browser stops
- Seamless experience for long answers (2-5 minutes)

**Code:** `frontend/script.js` - `shouldKeepListening` flag + `accumulatedTranscript`

### **3. Multi-Key API Management**
**Problem:** Free tier = 200 requests/day per project

**Solution:**
- Support multiple API keys from different projects
- Automatic rotation on rate limit detection
- 3 keys = 600 requests/day

**Code:** `backend/llm_client.py` - `API_KEYS` array + failover logic

### **4. Prompt Engineering Strategy**
**Approach:** Clear, concise prompts instead of verbose instructions

**Key Principles:**
- ONE question at a time
- Role-specific question types
- Clear text box usage rules (only for code/SQL)
- Natural conversation flow

**Code:** `backend/prompts.py` - Optimized from 158 lines to 87 lines

### **5. 70/30 Split Layout**
**Design Choice:**
- Left 30%: Text input for coding (always visible)
- Right 70%: Conversation + Timer + Status

**Rationale:** 
- Coding questions are common in tech interviews
- Dedicated space prevents UI switching
- Timer provides time awareness

### **6. Adaptive Persona Detection**
**Feature:** AI detects user behavior patterns

**Personas:**
- **Confused**: Simplifies questions, provides context
- **Efficient**: Quick pace, concise responses
- **Chatty**: Politely refocuses, summarizes
- **Edge Case**: Sets professional boundaries

**Code:** `backend/persona_logic.py` + prompt instructions

### **7. FastAPI over Flask**
**Reasons:**
- Async support for better performance
- Automatic data validation (Pydantic)
- Built-in OpenAPI documentation
- Modern Python features

### **8. In-Memory Session Store**
**Trade-off:** Simplicity vs Persistence

**Current:** Dictionary-based session storage
**Future:** PostgreSQL for user history tracking

---

## 📊 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML/CSS/JavaScript | UI and user interaction |
| **Voice** | Web Speech API | Speech recognition & synthesis |
| **Backend** | FastAPI (Python) | REST API and business logic |
| **AI Model** | Google Gemini 2.0 Flash | Conversational AI |
| **State** | In-memory dict | Session management |
| **Config** | python-dotenv | Environment variables |

---

## 📁 Project Structure

```
interview-practice-partner-039/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── llm_client.py        # Gemini API client (multi-key)
│   ├── prompts.py           # System prompts & templates
│   ├── persona_logic.py     # User behavior detection
│   └── audio_utils.py       # Resume parsing utilities
├── frontend/
│   ├── index.html           # Main UI (70/30 layout)
│   ├── style.css            # Styling & animations
│   └── script.js            # Voice/text handling + API calls
├── .env                     # API keys (gitignored)
├── .gitignore              # Ignore patterns
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🔧 Configuration

### **Environment Variables**

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | Primary Google Gemini API key |
| `GEMINI_API_KEY_2` | ❌ No | Secondary key for extended usage |
| `GEMINI_API_KEY_3` | ❌ No | Tertiary key for extended usage |

### **Interview Settings** (in code)

- **Max Questions**: 10 (configurable in `backend/main.py`)
- **Silence Timeout**: 15 seconds (in `frontend/script.js`)
- **Model**: `gemini-2.0-flash` (in `backend/llm_client.py`)

---

## 🐛 Troubleshooting

### **Rate Limit Errors**
- **Cause**: Exceeded 200 requests/day quota
- **Solution**: Add more API keys from different Google Cloud projects

### **Voice Not Working**
- **Cause**: Browser doesn't support Web Speech API
- **Solution**: Use Chrome or Edge browser

### **UI Not Updating**
- **Cause**: Browser cache
- **Solution**: Hard refresh (`Ctrl + Shift + R`)

### **Backend Not Starting**
- **Cause**: Missing dependencies or API key
- **Solution**: Run `pip install -r requirements.txt` and check `.env` file

---

## 🔮 Future Enhancements

- [ ] **Database Integration**: PostgreSQL for persistent user history
- [ ] **Advanced Analytics**: Track improvement over multiple sessions
- [ ] **Video Recording**: Record interview sessions for review
- [ ] **Multi-Language Support**: Conduct interviews in different languages
- [ ] **Custom Question Banks**: Allow users to add their own questions
- [ ] **Team Features**: Share feedback with mentors/coaches
- [ ] **Mobile App**: React Native version for on-the-go practice

---

## 📝 License

MIT License - Feel free to use and modify for your needs.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using Google Gemini AI**
