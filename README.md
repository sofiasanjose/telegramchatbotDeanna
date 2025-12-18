# Deanna - AI Personal Shopper Telegram Bot

An AI-powered Telegram chatbot that acts as your personal shopping assistant with a friendly, conversational personality.

## Features

- 💬 Natural conversation with AI-powered responses
- 🛍️ Personal shopping recommendations
- 🧠 Conversation memory (last 10 messages)
- ✨ Casual, friendly personality

## Setup

### Python Bot

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Create `.env` file:
```
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
```

3. Run:
```bash
python bot.py
```

### Node.js Bot (Alternative)

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (same as above)

3. Run:
```bash
npm start
```

## Commands

- `/start` - Start conversation with Deanna
- `/clear` - Clear conversation history

## Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token from @BotFather
- `OPENAI_API_KEY` - Your OpenAI API key
- `PORT` - Server port (default: 3001)
