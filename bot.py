#!/usr/bin/env python3
"""
Deanna Telegram Bot - AI Personal Shopper
"""
import os
import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')
user_conversations = {}

DEANNA_SYSTEM_PROMPT = """You are Deanna, an AI personal shopper and lifestyle curator. You talk like you're texting a close friend — super casual, warm, and real.

🎯 RULES:
- Text like a friend: short, natural, conversational AF
- 1-3 sentences MAX
- NO essays. NO lists. NO over-explaining.
- Emojis: 1-2 per message max (😊✨🙌💚)
- Ask quick follow-ups instead of dumping info
- Sound human, not robotic"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    await update.message.reply_text(
        "Hi! I'm Deanna — your AI personal shopper and lifestyle buddy. What's up? 💚 What can I help you find today?"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    await update.message.reply_text("✨ Memory cleared! Let's start fresh. What can I help you with?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    user_conversations[user_id].append({"role": "user", "content": user_message})
    
    if len(user_conversations[user_id]) > 10:
        user_conversations[user_id] = user_conversations[user_id][-10:]
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": DEANNA_SYSTEM_PROMPT},
                *user_conversations[user_id]
            ],
            max_tokens=50,
            temperature=0.9
        )
        
        deanna_response = response.choices[0].message.content
        user_conversations[user_id].append({"role": "assistant", "content": deanna_response})
        await update.message.reply_text(deanna_response)
        
    except Exception as e:
        logger.error(f"OpenAI Error: {e}")
        reply = random.choice(["Tell me more? 💚", "Interesting! Go on? ✨", "Love it! What else? 🙌"])
        user_conversations[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)

def main() -> None:
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🚀 Deanna bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
