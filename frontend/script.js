let sessionId = null;
let recognition = null;
let synth = window.speechSynthesis;
let isListening = false;
let resumeText = "";

const API_URL = "http://localhost:8000";

async function startInterview() {
    const role = document.getElementById("role-select").value;
    const experience = document.getElementById("experience-select").value;
    const resumeFile = document.getElementById("resume-upload").files[0];

    updateStatus("Initializing...");

    if (resumeFile) {
        const formData = new FormData();
        formData.append("file", resumeFile);
        try {
            updateStatus("Parsing Resume...");
            const res = await fetch(`${API_URL}/upload_resume`, { method: "POST", body: formData });
            const data = await res.json();
            resumeText = data.resume_text;
        } catch (err) {
            console.error("Resume upload failed", err);
        }
    }

    try {
        updateStatus("Starting Session...");
        const response = await fetch(`${API_URL}/start_session`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ role, experience_level: experience, resume_text: resumeText })
        });
        const data = await response.json();
        sessionId = data.session_id;

        document.getElementById("setup-screen").classList.add("hidden");
        document.getElementById("interview-screen").classList.remove("hidden");

        addMessage("agent", data.initial_message);
        speak(data.initial_message);
    } catch (err) {
        alert("Error: " + err);
    }
}

function addMessage(role, text) {
    const div = document.createElement("div");
    div.className = `message ${role}`;

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "agent" ? "Interviewer" : "You";
    div.appendChild(label);

    const content = document.createElement("div");
    content.textContent = text;
    div.appendChild(content);

    const history = document.getElementById("chat-history");
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
}

function updateStatus(text) {
    document.getElementById("status-text").textContent = text;

    const dot = document.getElementById("pulse-dot");
    if (text.includes("Listening")) {
        dot.className = "pulse-dot listening";
    } else if (text.includes("Speaking") || text.includes("Thinking")) {
        dot.className = "pulse-dot active";
    } else {
        dot.className = "pulse-dot";
    }
}

function speak(text) {
    if (synth.speaking) synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
        updateStatus("Agent Speaking...");
    };

    utterance.onend = () => {
        startListening();
    };

    synth.speak(utterance);
}

function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Web Speech API not supported. Please use Chrome/Edge.");
        return;
    }

    // Create recognition object only once (first time)
    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        // Set up error handler once
        recognition.onerror = (event) => {
            console.error("Speech error", event.error);
            if (event.error === 'aborted') {
                return; // Ignore aborted errors
            }
            if (event.error === 'no-speech') {
                updateStatus("No speech detected.");
            } else {
                updateStatus("Error: " + event.error);
            }
        };
    }

    let finalTranscript = '';
    let silenceTimer = null;
    const SILENCE_TIMEOUT = 15000; // 15 seconds of silence

    recognition.onstart = () => {
        isListening = true;
        updateStatus("Listening... (Auto-stops after 15s of silence)");
        document.getElementById('stop-listening-btn').style.display = 'block';
    };

    recognition.onresult = (event) => {
        // Clear existing silence timer since we detected speech
        if (silenceTimer) {
            clearTimeout(silenceTimer);
        }

        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript + ' ';
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        updateStatus(`Listening: ${finalTranscript} ${interimTranscript}`);

        // Start new silence timer - will auto-stop after 15s of no speech
        silenceTimer = setTimeout(() => {
            console.log("15 seconds of silence detected, auto-stopping...");
            if (recognition && isListening) {
                recognition.stop();
            }
        }, SILENCE_TIMEOUT);
    };

    recognition.onend = () => {
        isListening = false;
        if (silenceTimer) {
            clearTimeout(silenceTimer);
        }
        document.getElementById('stop-listening-btn').style.display = 'none';
        updateStatus("Processing...");

        if (finalTranscript.trim().length > 0) {
            sendUserResponse(finalTranscript);
        } else {
            updateStatus("Did not hear anything.");
        }
    };

    // Start recognition
    try {
        recognition.start();
    } catch (e) {
        console.error("Recognition start error:", e);
    }
}

function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
    }
}

async function sendUserResponse(text) {
    addMessage("user", text);
    updateStatus("Thinking...");

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, user_message: text })
        });

        const data = await response.json();

        if (data.is_interview_over) {
            addMessage("agent", data.agent_message);
            speak(data.agent_message);
            setTimeout(endInterview, 5000);
        } else {
            addMessage("agent", data.agent_message);
            speak(data.agent_message);
        }
    } catch (err) {
        console.error(err);
        updateStatus("Connection Error");
    }
}

async function endInterview() {
    // Stop recognition if still running
    if (recognition && isListening) {
        recognition.stop();
    }

    document.getElementById("interview-screen").classList.add("hidden");
    document.getElementById("feedback-screen").classList.remove("hidden");

    try {
        const response = await fetch(`${API_URL}/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, user_message: "" })
        });
        const data = await response.json();

        // Get the spoken feedback text
        const feedbackText = data.feedback.spoken_feedback || "No feedback available.";

        // Display it nicely
        document.getElementById("feedback-content").textContent = feedbackText;

        // Speak the feedback!
        if (synth.speaking) synth.cancel();
        const utterance = new SpeechSynthesisUtterance(feedbackText);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        synth.speak(utterance);

    } catch (err) {
        document.getElementById("feedback-content").textContent = "Error loading feedback.";
    }
}
