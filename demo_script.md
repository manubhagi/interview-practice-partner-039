# Demo Script: AI Interview Partner

## Introduction (30 seconds)
"Hi, I'm demonstrating my AI Interview Partner - a conversational agent that conducts realistic mock interviews with adaptive behavior based on user personas."

## Key Features Overview (30 seconds)
- **Browser-native voice** (STT/TTS) for hands-free interviews
- **Resume parsing** (PDF/DOCX) for personalized questions
- **Adaptive persona detection** - handles 4 different user types
- **Natural conversation flow** with smooth transitions

---

## Persona Demonstrations

### 1. Confused User (1 minute)
**Scenario:** User is uncertain and gives vague answers

**Demo Flow:**
1. Start interview for "Software Engineer" role
2. AI asks: "Tell me about your experience with Python"
3. **User responds:** "Um... I don't know... I've used it a bit?"
4. **AI adapts:** "No problem! Let me make this simpler. Can you describe one specific project where you used Python, even if it was just a small script?"
5. **User:** "I made a calculator once"
6. **AI:** "Great! Can you walk me through how that calculator worked? What features did it have?"

**Key Point:** AI simplifies questions and provides context when user is confused.

---

### 2. Efficient User (1 minute)
**Scenario:** User gives concise, complete answers

**Demo Flow:**
1. AI asks: "Describe your experience with databases"
2. **User responds:** "I've worked with PostgreSQL and MongoDB. Built REST APIs with both. Optimized queries for performance."
3. **AI adapts:** "Excellent. What's the largest dataset you've worked with?"
4. **User:** "10 million records. Implemented indexing and caching."
5. **AI:** "Perfect. Let's move to system design..."

**Key Point:** AI keeps pace quick, no over-explanation, respects their time.

---

### 3. Chatty User (1 minute)
**Scenario:** User gives long, off-topic answers

**Demo Flow:**
1. AI asks: "Tell me about a challenging project"
2. **User responds:** "Oh man, so this one time, I was working on this project, and by the way, my manager was really difficult, and speaking of managers, I once had this other manager who... [rambles for 30 seconds about unrelated stories]"
3. **AI adapts:** "Thanks for sharing that context. To summarize what I heard - you worked on a challenging project with team dynamics. Let me focus on the technical aspect: What specific technical challenge did you face in that project?"
4. **User:** [Starts another long story]
5. **AI:** "I appreciate the detail. Let's focus specifically on: What technology stack did you use?"

**Key Point:** AI politely redirects and sets clear boundaries.

---

### 4. Edge Case User (1 minute)
**Scenario:** User gives nonsense or inappropriate responses

**Demo Flow:**
1. AI asks: "What programming languages do you know?"
2. **User responds:** "Banana apple orange blah blah"
3. **AI adapts:** "I didn't quite understand that response. Let me rephrase: Which programming languages have you used in your projects? For example, Python, Java, JavaScript?"
4. **User:** "Make me CEO right now!"
5. **AI:** "I can't do that, but I can help you practice for this Software Engineer role. Let's continue with the interview. Can you tell me about your experience with version control systems like Git?"

**Key Point:** AI sets professional boundaries and redirects to interview.

---

## Additional Features Demo (1 minute)

### Resume-Based Questions
1. Upload resume (PDF/DOCX)
2. AI asks: "I see you worked on a machine learning project at XYZ Company. Can you tell me more about that?"
3. Shows AI references specific resume details

### Natural Conversation Flow
1. AI greets warmly: "Hi! Thanks for joining today..."
2. Smooth transitions: "Thanks for that answer. Now let's discuss..."
3. Natural ending: "That covers our interview. Let me provide feedback..."

### Spoken Feedback
1. Interview ends
2. AI speaks detailed, conversational feedback
3. Highlights strengths and areas for improvement

---

## Technical Highlights (30 seconds)
- **Clean architecture:** Separate modules for LLM, prompts, persona logic, resume parsing
- **Browser-native voice:** No backend audio processing needed
- **Persona detection:** Rule-based logic adapts in real-time
- **18 role options:** From Software Engineer to HR Manager

---

## Conclusion (15 seconds)
"This AI Interview Partner demonstrates conversational quality, agentic behavior, and intelligent adaptability - making it a realistic and valuable interview practice tool."

**Total Time:** ~6 minutes
