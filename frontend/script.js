let sessionId = null;
let recognition = null;
let synth = window.speechSynthesis;
let isListening = false;
let resumeText = "";
let interviewStartTime = null;
let timerInterval = null;
let shouldKeepListening = false;
let accumulatedTranscript = '';

const API_URL = "http://localhost:8000";

// Timer functions
function startTimer() {
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - interviewStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        const timerEl = document.getElementById('timer-display');
        if (timerEl) {
            timerEl.textContent = `⏱️ ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

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

        interviewStartTime = Date.now();
        startTimer();

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

    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onerror = (event) => {
            console.error("Speech error", event.error);
            if (event.error === 'aborted') return;

            // Auto-restart on network errors
            if (event.error === 'network' && shouldKeepListening) {
                console.log("Network error, restarting...");
                setTimeout(() => {
                    if (shouldKeepListening) {
                        recognition.start();
                    }
                }, 100);
                return;
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
    const SILENCE_TIMEOUT = 15000;

    // Enable auto-restart mode
    shouldKeepListening = true;
    accumulatedTranscript = '';

    recognition.onstart = () => {
        isListening = true;
        updateStatus("Listening... (Unlimited duration, stops after 15s silence)");
        document.getElementById('stop-listening-btn').style.display = 'block';
    };

    recognition.onresult = (event) => {
        if (silenceTimer) clearTimeout(silenceTimer);

        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript + ' ';
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }

        // Show accumulated + current transcript (truncated for display)
        const displayText = accumulatedTranscript + finalTranscript + interimTranscript;
        const truncated = displayText.length > 100 ? displayText.substring(0, 100) + '...' : displayText;
        updateStatus(`Listening: ${truncated}`);

        silenceTimer = setTimeout(() => {
            console.log("15 seconds of silence detected, stopping...");
            shouldKeepListening = false; // Disable auto-restart
            if (recognition && isListening) {
                recognition.stop();
            }
        }, SILENCE_TIMEOUT);
    };

    recognition.onend = () => {
        isListening = false;
        if (silenceTimer) clearTimeout(silenceTimer);

        // Add current transcript to accumulated
        accumulatedTranscript += finalTranscript;

        // Auto-restart if still should be listening (browser limit reached)
        if (shouldKeepListening && accumulatedTranscript.trim().length > 0) {
            console.log("Auto-restarting recognition for continuous speech...");
            finalTranscript = ''; // Reset for next segment
            setTimeout(() => {
                if (shouldKeepListening) {
                    try {
                        recognition.start();
                    } catch (e) {
                        console.error("Restart error:", e);
                    }
                }
            }, 100);
        } else {
            // Actually done listening
            document.getElementById('stop-listening-btn').style.display = 'none';
            updateStatus("Processing...");

            if (accumulatedTranscript.trim().length > 0) {
                sendUserResponse(accumulatedTranscript.trim());
                accumulatedTranscript = ''; // Clear for next time
            } else {
                updateStatus("Did not hear anything.");
            }
        }
    };

    try {
        recognition.start();
    } catch (e) {
        console.error("Recognition start error:", e);
    }
}

function stopListening() {
    shouldKeepListening = false; // Disable auto-restart
    if (recognition && isListening) {
        recognition.stop();
    }
}

function submitTextAnswer() {
    const textInput = document.getElementById('text-answer-input');
    const answer = textInput.value.trim();

    if (answer.length === 0) {
        alert("Please type your answer first!");
        return;
    }

    shouldKeepListening = false; // Disable auto-restart
    if (recognition && isListening) {
        recognition.stop();
    }

    textInput.value = '';
    sendUserResponse(answer);
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
    shouldKeepListening = false;
    if (recognition && isListening) {
        recognition.stop();
    }

    stopTimer();

    if (synth.speaking) synth.cancel();

    document.getElementById("interview-screen").classList.add("hidden");
    document.getElementById("feedback-screen").classList.remove("hidden");

    try {
        const response = await fetch(`${API_URL}/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, user_message: "" })
        });
        const data = await response.json();

        const feedbackText = data.feedback.spoken_feedback || "No feedback available.";

        document.getElementById("feedback-content").innerHTML = feedbackText.replace(/\n/g, '<br>');

    } catch (err) {
        document.getElementById("feedback-content").textContent = "Error loading feedback.";
    }
}
