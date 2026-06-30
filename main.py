from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot import ChatBot
import uuid

app = FastAPI(title="AI Water Management Chatbot", description="Intelligent water management assistant")

# Initialize bot
bot = ChatBot()

# Store sessions
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    domain: str
    confidence: float
    suggestions: list
    timestamp: str
    context: dict = {}

@app.get("/", response_class=HTMLResponse)
async def get_chat_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💧 AI Water Management Assistant</title>
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --black:        #0a0a0a;
                --black-soft:   #111111;
                --black-card:   #161616;
                --black-border: #222222;
                --black-hover:  #1e1e1e;
                --orange:       #ff6a00;
                --orange-dim:   #cc5500;
                --orange-glow:  rgba(255,106,0,0.18);
                --orange-faint: rgba(255,106,0,0.07);
                --text-primary: #f0f0f0;
                --text-muted:   #888888;
                --text-dim:     #555555;
            }

            * { margin:0; padding:0; box-sizing:border-box; }

            body {
                font-family: 'Syne', sans-serif;
                background: var(--black);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 16px;
                overflow-x: hidden;
            }

            body::before {
                content: '';
                position: fixed;
                inset: 0;
                background-image:
                    linear-gradient(rgba(255,106,0,0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,106,0,0.03) 1px, transparent 1px);
                background-size: 48px 48px;
                pointer-events: none;
                z-index: 0;
            }

            body::after {
                content: '';
                position: fixed;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(255,106,0,0.10) 0%, transparent 70%);
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                pointer-events: none;
                z-index: 0;
            }

            .chat-wrapper {
                position: relative;
                z-index: 1;
                width: 100%;
                max-width: 960px;
                height: 90vh;
                background: var(--black-card);
                border: 1px solid var(--black-border);
                border-radius: 20px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow:
                    0 0 0 1px rgba(255,106,0,0.06),
                    0 40px 80px rgba(0,0,0,0.8),
                    inset 0 1px 0 rgba(255,255,255,0.04);
            }

            /* HEADER */
            .chat-header {
                background: var(--black-soft);
                padding: 18px 28px;
                border-bottom: 1px solid var(--black-border);
                display: flex;
                align-items: center;
                gap: 16px;
                position: relative;
                overflow: hidden;
                flex-shrink: 0;
            }

            .chat-header::after {
                content: '';
                position: absolute;
                bottom: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--orange), transparent);
            }

            .bot-avatar {
                width: 46px;
                height: 46px;
                border-radius: 12px;
                background: linear-gradient(135deg, var(--orange), var(--orange-dim));
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
                flex-shrink: 0;
                box-shadow: 0 4px 16px rgba(255,106,0,0.35);
            }

            .header-text h1 {
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--text-primary);
                letter-spacing: -0.02em;
            }

            .header-text p {
                font-size: 0.75rem;
                color: var(--text-muted);
                font-family: 'DM Mono', monospace;
                font-weight: 300;
                margin-top: 2px;
            }

            .status-pill {
                margin-left: auto;
                display: flex;
                align-items: center;
                gap: 7px;
                background: rgba(255,106,0,0.1);
                border: 1px solid rgba(255,106,0,0.2);
                color: var(--orange);
                padding: 6px 14px;
                border-radius: 99px;
                font-size: 0.72rem;
                font-family: 'DM Mono', monospace;
                font-weight: 500;
            }

            .status-dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: var(--orange);
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(255,106,0,0.5); }
                50%      { opacity:0.7; box-shadow: 0 0 0 4px rgba(255,106,0,0); }
            }

            /* MESSAGES */
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 28px 28px 12px;
                scroll-behavior: smooth;
                background: var(--black-card);
            }

            .chat-messages::-webkit-scrollbar { width: 4px; }
            .chat-messages::-webkit-scrollbar-track { background: transparent; }
            .chat-messages::-webkit-scrollbar-thumb {
                background: var(--black-border);
                border-radius: 2px;
            }
            .chat-messages::-webkit-scrollbar-thumb:hover { background: var(--orange-dim); }

            .message {
                margin-bottom: 24px;
                animation: fadeUp 0.25s ease both;
            }

            @keyframes fadeUp {
                from { opacity:0; transform:translateY(12px); }
                to   { opacity:1; transform:translateY(0); }
            }

            .message.user { display:flex; justify-content:flex-end; }
            .message.bot  { display:flex; justify-content:flex-start; }

            .message-content { max-width: 74%; }

            .bubble {
                padding: 14px 18px;
                border-radius: 16px;
                line-height: 1.65;
                font-size: 0.93rem;
            }

            .message.user .bubble {
                background: linear-gradient(135deg, var(--orange), var(--orange-dim));
                color: #fff;
                border-bottom-right-radius: 4px;
                font-weight: 500;
                box-shadow: 0 4px 20px rgba(255,106,0,0.3);
            }

            .message.bot .bubble {
                background: var(--black-soft);
                color: var(--text-primary);
                border: 1px solid var(--black-border);
                border-bottom-left-radius: 4px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.4);
            }

            .message.bot .bubble strong { color: var(--orange); }

            .message.bot .bubble ul {
                margin: 10px 0 4px 18px;
            }

            .message.bot .bubble li {
                margin: 5px 0;
                color: var(--text-primary);
            }

            .domain-tag {
                font-size: 0.68rem;
                margin-top: 6px;
                margin-left: 8px;
                color: var(--text-dim);
                display: flex;
                align-items: center;
                gap: 8px;
                font-family: 'DM Mono', monospace;
                font-weight: 400;
                letter-spacing: 0.03em;
            }

            .confidence-badge {
                background: var(--black-hover);
                border: 1px solid var(--black-border);
                color: var(--text-muted);
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.64rem;
            }

            /* SUGGESTIONS */
            .suggestions {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 12px;
                margin-left: 8px;
            }

            .suggestion-chip {
                background: transparent;
                border: 1px solid var(--black-border);
                color: var(--text-muted);
                padding: 7px 14px;
                border-radius: 8px;
                font-size: 0.8rem;
                font-family: 'Syne', sans-serif;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.18s ease;
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .suggestion-chip:hover {
                background: var(--orange-faint);
                border-color: rgba(255,106,0,0.4);
                color: var(--orange);
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(255,106,0,0.15);
            }

            /* QUICK ACTIONS */
            .quick-actions {
                padding: 12px 20px;
                background: var(--black-soft);
                border-top: 1px solid var(--black-border);
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                flex-shrink: 0;
            }

            .quick-btn {
                background: var(--black-card);
                border: 1px solid var(--black-border);
                color: var(--text-muted);
                padding: 6px 14px;
                border-radius: 8px;
                font-size: 0.77rem;
                font-family: 'Syne', sans-serif;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.18s;
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .quick-btn i { font-size: 0.7rem; color: var(--orange); }

            .quick-btn:hover {
                background: var(--orange-faint);
                border-color: rgba(255,106,0,0.35);
                color: var(--orange);
                transform: translateY(-1px);
            }

            /* INPUT AREA */
            .chat-input {
                padding: 16px 20px;
                background: var(--black-soft);
                border-top: 1px solid var(--black-border);
                display: flex;
                gap: 10px;
                align-items: center;
                flex-shrink: 0;
            }

            .input-wrapper { flex: 1; position: relative; }

            .chat-input input {
                width: 100%;
                padding: 13px 20px;
                background: var(--black-card);
                border: 1px solid var(--black-border);
                border-radius: 12px;
                font-size: 0.92rem;
                font-family: 'Syne', sans-serif;
                color: var(--text-primary);
                outline: none;
                transition: all 0.2s;
                caret-color: var(--orange);
            }

            .chat-input input::placeholder { color: var(--text-dim); }

            .chat-input input:focus {
                border-color: rgba(255,106,0,0.5);
                box-shadow: 0 0 0 3px rgba(255,106,0,0.08);
                background: var(--black-hover);
            }

            .send-btn {
                width: 48px;
                height: 48px;
                border-radius: 12px;
                background: linear-gradient(135deg, var(--orange), var(--orange-dim));
                color: white;
                border: none;
                cursor: pointer;
                font-size: 1rem;
                transition: all 0.18s;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                box-shadow: 0 4px 16px rgba(255,106,0,0.3);
            }

            .send-btn:hover {
                transform: scale(1.06);
                box-shadow: 0 6px 24px rgba(255,106,0,0.45);
            }

            .send-btn:active { transform: scale(0.95); }

            /* TYPING INDICATOR */
            .typing-indicator {
                padding: 14px 18px;
                background: var(--black-soft);
                border: 1px solid var(--black-border);
                border-radius: 16px;
                border-bottom-left-radius: 4px;
                width: fit-content;
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .typing-indicator span {
                display: inline-block;
                width: 7px;
                height: 7px;
                background: var(--orange);
                border-radius: 50%;
                opacity: 0.5;
                animation: bounce 1.2s infinite;
            }

            .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
            .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes bounce {
                0%,60%,100% { transform:translateY(0); opacity:0.5; }
                30% { transform:translateY(-8px); opacity:1; }
            }

            @media (max-width: 768px) {
                body { padding: 8px; }
                .chat-wrapper { height: 97vh; border-radius: 14px; }
                .message-content { max-width: 88%; }
                .header-text h1 { font-size: 0.95rem; }
                .status-pill { display: none; }
                .chat-messages { padding: 16px; }
                .quick-actions { padding: 10px 14px; }
                .chat-input { padding: 12px 14px; }
            }
        </style>
    </head>
    <body>
        <div class="chat-wrapper">
            <div class="chat-header">
                <div class="bot-avatar">💧</div>
                <div class="header-text">
                    <h1>Water Management Assistant</h1>
                    <p>conservation · quality · smart tech</p>
                </div>
                <div class="status-pill">
                    <div class="status-dot"></div>
                    ONLINE
                </div>
            </div>

            <div class="chat-messages" id="chat-messages">
                <div class="message bot">
                    <div class="message-content">
                        <div class="bubble">
                            <strong>👋 Welcome!</strong><br><br>
                            I'm here to help you with:
                            <ul>
                                <li>💧 <strong>Water Conservation</strong> — Save water at home & garden</li>
                                <li>🔬 <strong>Water Quality</strong> — Testing, filtration & treatment</li>
                                <li>📊 <strong>Usage Monitoring</strong> — Track consumption & find leaks</li>
                                <li>🌧️ <strong>Rainwater Harvesting</strong> — Collect and store rain</li>
                                <li>🌫️ <strong>Fog Collection</strong> — Harvest water from air</li>
                                <li>🤖 <strong>Smart Water Tech</strong> — IoT sensors & AI solutions</li>
                            </ul>
                            What would you like to know today?
                        </div>
                        <div class="domain-tag">
                            <i class="fas fa-robot"></i> AI Assistant
                        </div>
                    </div>
                </div>
            </div>

            <div class="quick-actions">
                <button class="quick-btn" onclick="quickAsk('How can I save water at home?')">
                    <i class="fas fa-home"></i> Save at Home
                </button>
                <button class="quick-btn" onclick="quickAsk('How to test water quality?')">
                    <i class="fas fa-flask"></i> Water Quality
                </button>
                <button class="quick-btn" onclick="quickAsk('How to find water leaks?')">
                    <i class="fas fa-wrench"></i> Find Leaks
                </button>
                <button class="quick-btn" onclick="quickAsk('What is rainwater harvesting?')">
                    <i class="fas fa-cloud-rain"></i> Rain Harvesting
                </button>
                <button class="quick-btn" onclick="quickAsk('How does fog harvesting work?')">
                    <i class="fas fa-cloud"></i> Fog Collection
                </button>
            </div>

            <div class="chat-input">
                <div class="input-wrapper">
                    <input type="text" id="user-input"
                           placeholder="Ask anything about water management…"
                           onkeypress="if(event.key==='Enter') sendMessage()">
                </div>
                <button class="send-btn" onclick="sendMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>

        <script>
            let sessionId = localStorage.getItem('chat_session_id');
            if (!sessionId) {
                sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('chat_session_id', sessionId);
            }

            async function sendMessage() {
                const input = document.getElementById('user-input');
                const message = input.value.trim();
                if (!message) return;

                addMessage(message, 'user');
                input.value = '';
                showTypingIndicator();

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ message, session_id: sessionId })
                    });
                    const data = await response.json();
                    hideTypingIndicator();
                    addBotMessage(data);
                } catch (error) {
                    hideTypingIndicator();
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            }

            function addMessage(text, sender) {
                const container = document.getElementById('chat-messages');
                const msgDiv = document.createElement('div');
                msgDiv.className = `message ${sender}`;

                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';

                const bubbleDiv = document.createElement('div');
                bubbleDiv.className = 'bubble';
                bubbleDiv.innerHTML = text.replace(/\\n/g, '<br>');
                contentDiv.appendChild(bubbleDiv);

                if (sender === 'bot') {
                    const domainTag = document.createElement('div');
                    domainTag.className = 'domain-tag';
                    domainTag.innerHTML = '<i class="fas fa-robot"></i> AI Assistant';
                    contentDiv.appendChild(domainTag);
                }

                msgDiv.appendChild(contentDiv);
                container.appendChild(msgDiv);
                container.scrollTop = container.scrollHeight;
            }

            function addBotMessage(data) {
                const container = document.getElementById('chat-messages');
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message bot';

                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';

                const bubbleDiv = document.createElement('div');
                bubbleDiv.className = 'bubble';
                bubbleDiv.innerHTML = data.response.replace(/\\n/g, '<br>');
                contentDiv.appendChild(bubbleDiv);

                const domainTag = document.createElement('div');
                domainTag.className = 'domain-tag';
                const confidencePercent = Math.round(data.confidence * 100);
                domainTag.innerHTML = `
                    <i class="fas fa-tag"></i>
                    ${data.domain.replace('water_management_', '').replace(/_/g, ' ').toUpperCase()}
                    <span class="confidence-badge"><i class="fas fa-chart-line"></i> ${confidencePercent}%</span>
                `;
                contentDiv.appendChild(domainTag);

                if (data.suggestions && data.suggestions.length > 0) {
                    const suggestionsDiv = document.createElement('div');
                    suggestionsDiv.className = 'suggestions';
                    data.suggestions.forEach(s => {
                        const chip = document.createElement('button');
                        chip.className = 'suggestion-chip';
                        chip.innerHTML = `<i class="fas fa-lightbulb"></i> ${s}`;
                        chip.onclick = () => quickAsk(s);
                        suggestionsDiv.appendChild(chip);
                    });
                    contentDiv.appendChild(suggestionsDiv);
                }

                msgDiv.appendChild(contentDiv);
                container.appendChild(msgDiv);
                container.scrollTop = container.scrollHeight;
            }

            function quickAsk(text) {
                document.getElementById('user-input').value = text;
                sendMessage();
            }

            function showTypingIndicator() {
                const container = document.getElementById('chat-messages');
                const typingDiv = document.createElement('div');
                typingDiv.id = 'typing-indicator';
                typingDiv.className = 'message bot';
                typingDiv.innerHTML = `
                    <div class="message-content">
                        <div class="typing-indicator">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                `;
                container.appendChild(typingDiv);
                container.scrollTop = container.scrollHeight;
            }

            function hideTypingIndicator() {
                const el = document.getElementById('typing-indicator');
                if (el) el.remove();
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handle chat messages with session support"""
    result = bot.chat(request.message, request.session_id)
    return ChatResponse(**result)

@app.get("/api/stats")
async def get_stats():
    """Get chatbot statistics"""
    return {
        "total_queries": bot.stats["total_queries"],
        "domains": bot.stats["domains_handled"],
        "water_stats": bot.get_water_stats()
    }

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session summary"""
    return bot.get_session_summary(session_id)

@app.delete("/api/history")
async def clear_history():
    """Clear conversation history"""
    return bot.clear_history()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)