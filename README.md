# 💧 Agribot — AI Water Management Chatbot
 Live Demo : [AgribotAI](https://elegant-clafoutis-4f6de1.netlify.app/)


Agribot is an intelligent, rule-based chatbot built with **FastAPI** that answers questions about water conservation, water quality, usage monitoring, rainwater and fog harvesting, smart water technology, and regulations. It ships with a polished, dark-themed chat UI served directly from the backend — no separate frontend build required.

## Features

- **Domain-aware responses** across 7 water management topics: conservation, quality, usage monitoring, rainwater harvesting, fog harvesting, smart tech, and regulations
- **Weighted keyword intent detection** with confidence scoring for each response
- **Contextual extraction** of numbers, settings (home/garden/farm/etc.), and climate hints from queries
- **Smart follow-up suggestions** tailored to the detected topic and keywords
- **Conversational extras**: greetings, farewells, jokes, water facts, quotes, identity/help responses, emergency water guidance, and a 7-day water-saving challenge
- **Session-based context tracking** so each conversation's history and domains discussed can be summarized
- **Built-in single-page chat UI** (HTML/CSS/JS) with quick-action buttons, typing indicator, and suggestion chips
- **REST API** for chat, stats, session summaries, and history clearing

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework and API
- [Pydantic](https://docs.pydantic.dev/) — request/response validation
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- Vanilla HTML/CSS/JS for the embedded chat interface

## Project Structure

```
water_management_chat-bot-main/
├── main.py             # FastAPI app, routes, and embedded chat UI
├── chatbot.py           # Chatbot engine: knowledge base, intent detection, response logic
├── requirements.txt     # Python dependencies
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd water_management_chat-bot-main

# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open **http://localhost:8000** in your browser to use the chat interface.

## API Reference

### `GET /`
Serves the chat UI (HTML page).

### `POST /api/chat`
Send a message to the bot.

**Request body:**
```json
{
  "message": "How can I save water at home?",
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "response": "💧 Top Water Conservation Tips: ...",
  "domain": "water_management_water_conservation",
  "confidence": 0.83,
  "suggestions": ["How can I detect hidden leaks?", "..."],
  "timestamp": "2026-06-30T12:00:00",
  "context": {}
}
```

### `GET /api/stats`
Returns chatbot usage statistics: total queries, domains handled, and quick-reference water stats.

### `GET /api/session/{session_id}`
Returns a summary of a given session: number of exchanges, last query, and domains discussed.

### `DELETE /api/history`
Clears all conversation history and session context.

## Topics You Can Ask About

| Topic | Example Question |
|---|---|
| 🌿 Water Conservation | "How can I save water at home?" |
| 🔬 Water Quality | "How do I test my water quality?" |
| 📊 Usage Monitoring | "How much water does the average household use?" |
| 🌧️ Rainwater Harvesting | "How does rainwater harvesting work?" |
| 🌫️ Fog Harvesting | "What is fog harvesting?" |
| 🤖 Smart Water Tech | "What are smart water meters?" |
| ⚖️ Regulations | "What are EPA water standards?" |
| 💬 Just for Fun | "Tell me a joke", "Water fact", "Water quote" |

## How It Works

1. **Intent detection** — incoming messages are scored against weighted keyword lists (primary and specific keywords) for each domain to determine the most likely topic and a confidence score.
2. **Response generation** — each domain has a dedicated handler that inspects the query for specific sub-topics (e.g., "shower", "leak", "pH", "lead") and returns a tailored, formatted answer from the knowledge base.
3. **Fallback handling** — if no domain matches strongly, the bot checks for conversational intents (greetings, thanks, jokes, facts, emergencies, etc.) before falling back to a general help message.
4. **Suggestions & context** — each response includes follow-up question suggestions and any extracted context (numbers, setting, climate) to keep the conversation flowing naturally.
