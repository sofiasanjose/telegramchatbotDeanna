#!/usr/bin/env python3
"""
Deanna Telegram Bot - Python Version with Ministore
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from dotenv import load_dotenv
from analyzer import ConversationAnalyzer
from ministore import MinistoreGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Store conversations in memory
user_conversations = {}

DEANNA_SYSTEM_PROMPT = """You are Deanna, an AI personal shopper and lifestyle curator. You talk like you're texting a close friend — super casual, warm, and real.

🎯 RULES:
- Text like a friend: short, natural, conversational AF
- 1-3 sentences MAX
- NO essays. NO lists. NO over-explaining.
- Emojis: 1-2 per message max (😊✨🙌💚)
- Ask quick follow-ups instead of dumping info
- Sound human, not robotic

Introduction: "Hi! I'm Deanna — your AI personal shopper and lifestyle buddy. What's up? 💚 What can I help you find today?"
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    
    await update.message.reply_text(
        "Hi! I'm Deanna — your AI personal shopper and lifestyle buddy. What's up? 💚 What can I help you find today?"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear conversation history."""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    
    await update.message.reply_text(
        "✨ Memory cleared! Let's start fresh. What can I help you with?"
    )

async def ministore(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Force create a ministore from current conversation."""
    user_id = update.effective_user.id
    
    if user_id not in user_conversations or len(user_conversations[user_id]) == 0:
        await update.message.reply_text(
            "We haven't chatted about any products yet! Tell me what you're looking for first 😊"
        )
        return
    
    # Get full conversation text
    conversation_text = '\n'.join([msg['content'] for msg in user_conversations[user_id]])
    
    # Extract products
    products = ConversationAnalyzer.extract_products(conversation_text)
    
    if len(products) == 0:
        await update.message.reply_text(
            "I didn't catch any specific products in our chat! Tell me what you're interested in 💚"
        )
        return
    
    await update.message.reply_text(
        f"✨ Creating your ministore with {len(products)} products! Give me a sec..."
    )
    
    try:
        generator = MinistoreGenerator()
        title = f"Deanna's Picks - {update.effective_user.first_name}"
        
        result = generator.create_ministore(title, products)
        generator.disconnect()
        
        if result:
            await update.message.reply_text(
                f"🎉 Your ministore is ready!\n\n"
                f"📦 {result['num_products']} products picked just for you\n"
                f"🔗 {result['url']}\n\n"
                f"Happy shopping! 💚"
            )
        else:
            await update.message.reply_text(
                "Oops, couldn't create the ministore right now. Try again? 🙏"
            )
    except Exception as e:
        logger.error(f"Ministore creation error: {e}")
        await update.message.reply_text(
            "Something went wrong creating your ministore! Try again in a bit? 🙏"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Initialize conversation if needed
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    # Add user message to conversation
    user_conversations[user_id].append({"role": "user", "content": user_message})
    
    # Keep only last 10 messages
    if len(user_conversations[user_id]) > 10:
        user_conversations[user_id] = user_conversations[user_id][-10:]
    
    try:
        # Call OpenAI
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
        
        # Check if we should auto-create ministore
        conversation_text = '\n'.join([msg['content'] for msg in user_conversations[user_id]])
        if ConversationAnalyzer.should_create_ministore(conversation_text):
            products = ConversationAnalyzer.extract_products(conversation_text)
            await update.message.reply_text(
                f"💚 I've got {len(products)} items for you! Want me to create a ministore? Type /ministore"
            )
        
    except Exception as e:
        logger.error(f"OpenAI Error: {e}")
        # Fallback responses
        fallbacks = [
            "Tell me more? 💚",
            "Interesting! Go on? ✨",
            "Love it! What else? 🙌",
        ]
        import random
        reply = random.choice(fallbacks)
        user_conversations[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler("ministore", ministore))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run the bot
    logger.info("🚀 Deanna bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
