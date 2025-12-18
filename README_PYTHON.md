# Deanna Ministore Bot

A Telegram bot that creates personalized shopping ministores based on conversational product recommendations.

## Features

- 🤖 **AI-Powered Chat**: OpenAI GPT-4o-mini integration for natural conversations
- 🛍️ **Product Detection**: Automatically identifies products in conversations
- 📦 **Ministore Generation**: Creates curated shopping collections via SerperDev API
- 💾 **MySQL Integration**: Stores ministores in database for deanna2u.com
- ⚡ **Long Polling**: Reliable bot operation without webhooks

## Architecture

```
bot.py          - Main Telegram bot with OpenAI integration
analyzer.py     - Product extraction from conversations  
ministore.py    - SerperDev API + MySQL ministore creation
.env            - Environment variables (API keys, database credentials)
```

## Setup

### 1. Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install python-telegram-bot==21.7 openai python-dotenv mysql-connector-python requests
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# SerperDev API (Google Shopping)
SERPER_API_KEY=your_serper_api_key

# MySQL Database
DB_HOST=your_database_host
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
DB_DATABASE=your_database_name

# Base URL for ministores
BASE_URL=https://www.deanna2u.com
```

### 4. Run the Bot

```bash
python bot.py
```

## Bot Commands

- `/start` - Initialize conversation
- `/clear` - Clear conversation history
- `/ministore` - Create ministore from conversation

## How It Works

1. **Chat with Deanna**: User asks for product recommendations
2. **Product Detection**: Bot analyzes conversation for brands and product types
3. **Auto-Suggestion**: When 3+ products detected, suggests creating ministore
4. **SerperDev Search**: Fetches real products from Google Shopping
5. **Database Storage**: Saves ministore to MySQL (cliperest_book + cliperest_clipping tables)
6. **URL Generation**: Returns shareable ministore link

## Database Schema

### cliperest_book
- `id` - Auto-increment primary key
- `user_id` - User who created the ministore (237 for Sofia)
- `name` - Ministore title
- `slug` - URL-friendly identifier
- `numClips` - Number of products
- `rendered`, `privacy`, `created`, etc.

### cliperest_clipping
- `id` - Auto-increment primary key
- `book_id` - Foreign key to cliperest_book
- `caption` - Product title
- `text` - Price and source
- `thumbnail` - Product image URL
- `url` - Product link
- `created`, `modified`, etc.

## Configuration

### User ID
Ministores are created under user ID **237** (Sofia Claudia-San Jose Bonoan).  
To change, edit `ministore.py` line 94:
```python
cursor.execute(book_query, (title, now, now, 0, slug, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 237))
                                                                                      ^^^ Change this
```

### Username
URL format uses underscored username.  
To change, edit `ministore.py` line 117:
```python
username = "sofia_claudia_san_jose_bonoan"  # Change this
```

## Troubleshooting

### Bot not responding
- Check if bot is running: `ps aux | grep bot.py`
- Kill existing instances: `pkill -9 -f "python.*bot.py"`
- Restart: `python bot.py`

### Ministore not showing on website
- Verify database connection (check `.env` credentials)
- Check if book was created: Query `cliperest_book` table
- Ensure `user_id` matches your account
- Verify `rendered=1` and `numClips > 0`

### Network errors
- Bot uses long polling (no webhooks needed)
- Handles network interruptions automatically
- Check internet connection if persistent issues

## API Limits

- **OpenAI**: max_tokens=50, temperature=0.9
- **SerperDev**: Free tier has API call limits
- **Telegram**: No rate limits with long polling

## Development

### Add new product types
Edit `analyzer.py`:
```python
PRODUCT_TYPES = [
    'shoes', 'shirt', 'jeans',  # Add more here
]
```

### Add new brands
Edit `analyzer.py`:
```python
BRANDS = [
    'nike', 'adidas', 'zara',  # Add more here
]
```

### Change bot personality
Edit `bot.py` OpenAI system message:
```python
{
    "role": "system",
    "content": "Your new personality here..."
}
```

## License

Private project for deanna2u.com

## Support

Contact: bonoansofia@gmail.com
