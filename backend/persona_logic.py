"""
Persona detection and handling logic for adaptive interview behavior.
"""

def detect_persona(user_message: str, conversation_history: list) -> str:
    """
    Detects user persona based on their response patterns.
    
    Returns: "confused", "efficient", "chatty", "edge", or "normal"
    """
    message_lower = user_message.lower().strip()
    word_count = len(user_message.split())
    
    # Edge Case Detection
    edge_keywords = ["make me ceo", "give me job", "hire me now", "your weights", "your model", 
                     "banana", "asdfgh", "blah blah", "random gibberish"]
    if any(keyword in message_lower for keyword in edge_keywords):
        return "edge"
    
    if word_count < 3 and not any(word in message_lower for word in ["yes", "no", "okay", "sure"]):
        return "edge"
    
    # Confused Detection
    confused_keywords = ["i don't know", "not sure", "what do you mean", "don't understand", 
                        "confused", "unclear", "help", "what is", "explain"]
    if any(keyword in message_lower for keyword in confused_keywords):
        return "confused"
    
    # Very short answers repeatedly
    if word_count <= 5:
        # Check history for pattern of short answers
        recent_user_messages = [msg["content"] for msg in conversation_history[-6:] if msg["role"] == "user"]
        if len(recent_user_messages) >= 2:
            avg_length = sum(len(m.split()) for m in recent_user_messages) / len(recent_user_messages)
            if avg_length < 8:
                return "confused"
    
    # Efficient Detection
    if 5 < word_count <= 25:
        # Concise but complete
        return "efficient"
    
    # Chatty Detection
    if word_count > 100:
        return "chatty"
    
    # Check for off-topic rambling
    if word_count > 60:
        offtopic_keywords = ["by the way", "also", "speaking of", "reminds me", "funny story"]
        if any(keyword in message_lower for keyword in offtopic_keywords):
            return "chatty"
    
    return "normal"


def get_persona_instruction(persona: str) -> str:
    """
    Returns specific instructions for handling detected persona.
    """
    instructions = {
        "confused": """
The user seems confused or uncertain. 
- Simplify your next question
- Provide a bit more context
- Be supportive and encouraging
- Consider rephrasing if they're stuck on the same question
""",
        "efficient": """
The user is being concise and efficient.
- Keep your questions brief and to the point
- Don't over-explain
- Move through topics quickly
- Respect their time
""",
        "chatty": """
The user is giving very long or off-topic answers.
- Politely acknowledge their answer
- Summarize the key point you heard
- Redirect to a specific, focused question
- Set clear boundaries: "Let's focus on..."
""",
        "edge": """
The user gave an irrelevant, nonsense, or inappropriate response.
- Politely set a boundary
- Explain what you can and cannot do
- Redirect back to the interview
- Example: "I can't do that, but I can help you practice for this role. Let's continue..."
""",
        "normal": """
The user is responding normally.
- Continue with standard interview flow
- Ask follow-ups if answer lacks depth
- Move to next topic if answer is complete
"""
    }
    return instructions.get(persona, instructions["normal"])
