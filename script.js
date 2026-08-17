document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBody = document.getElementById("chat-body");
    const clearBtn = document.getElementById("clear-btn");
    const initialTime = document.getElementById("initial-time");

    if (initialTime) {
        initialTime.textContent = getCurrentTime();
    }

    // Load session chat history if available
    loadChatHistory();

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (message) {
            handleSendMessage(message);
        }
    });

    clearBtn.addEventListener("click", () => {
        if (confirm("Clear current session chat history?")) {
            sessionStorage.removeItem("chatHistory");
            chatBody.innerHTML = `
                <div class="message bot-message">
                    <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
                    <div class="msg-content">
                        <p>Chat cleared! How can I help you now?</p>
                        <span class="timestamp">${getCurrentTime()}</span>
                    </div>
                </div>
            `;
        }
    });

    function handleSendMessage(messageText) {
        // Render user message bubble
        appendMessage(messageText, "user");
        userInput.value = "";

        // Show typing indicator
        const typingId = showTypingIndicator();

        // Call Flask API endpoint
        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator(typingId);
            if (data.status === "success") {
                appendMessage(data.response, "bot", data.intent, data.confidence);
            } else {
                appendMessage("Sorry, an error occurred while processing your request.", "bot");
            }
        })
        .catch(error => {
            removeTypingIndicator(typingId);
            console.error("API Error:", error);
            appendMessage("Unable to reach the server. Please check your connection.", "bot");
        });
    }

    function appendMessage(text, sender, intent = null, confidence = null) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", `${sender}-message`);

        const avatarDiv = document.createElement("div");
        avatarDiv.classList.add("msg-avatar");
        avatarDiv.innerHTML = sender === "user" 
            ? `<i class="fa-solid fa-user"></i>` 
            : `<i class="fa-solid fa-robot"></i>`;

        const contentDiv = document.createElement("div");
        contentDiv.classList.add("msg-content");
        
        let metaHtml = "";
        if (sender === "bot" && intent && confidence !== null) {
            metaHtml = `<div style="font-size: 0.65rem; color: #64748b; margin-top: 4px;">Detected Intent: <i>${intent}</i> (${Math.round(confidence * 100)}%)</div>`;
        }

        contentDiv.innerHTML = `<p>${text}</p>${metaHtml}<span class="timestamp">${getCurrentTime()}</span>`;

        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(contentDiv);
        chatBody.appendChild(msgDiv);

        scrollToBottom();
        saveChatHistory();
    }

    function showTypingIndicator() {
        const id = "typing-" + Date.now();
        const typingDiv = document.createElement("div");
        typingDiv.classList.add("message", "bot-message");
        typingDiv.id = id;

        typingDiv.innerHTML = `
            <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="msg-content">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatBody.appendChild(typingDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function saveChatHistory() {
        sessionStorage.setItem("chatHistory", chatBody.innerHTML);
    }

    function loadChatHistory() {
        const savedHistory = sessionStorage.getItem("chatHistory");
        if (savedHistory) {
            chatBody.innerHTML = savedHistory;
            scrollToBottom();
        }
    }

    // Expose quick query handler globally for click events
    window.sendQuickQuery = function(text) {
        handleSendMessage(text);
    };
});
