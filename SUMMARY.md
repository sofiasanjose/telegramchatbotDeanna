# Repository Summary

## What This Is
Python Telegram bot (@DeannaChat_bot) that creates shopping ministores from conversations.

## What Works ✅
- **Bot**: Responds via OpenAI GPT-4o-mini
- **Product Detection**: Extracts brands/items from chat
- **Database**: Saves ministores to MySQL
- **Commands**: /start, /clear, /ministore

## What Doesn't Work ❌
- **URLs**: Ministores save to database but don't display on deanna2u.com website
- **Issue**: Website routing/caching problem, not bot code

## Repository Status
- ✅ Clean Python code only
- ✅ Proper .gitignore
- ✅ Documentation (README_PYTHON.md, QUICKSTART.md)
- ✅ Requirements.txt
- ✅ Git initialized with 2 commits
- ❌ Not pushed to GitHub yet (needs remote)

## File Structure
```
deanna-ministore-system/
├── bot.py              # Main bot (OpenAI + Telegram)
├── analyzer.py         # Product extractor
├── ministore.py        # SerperDev + MySQL
├── requirements.txt    # Python dependencies
├── .env               # API keys (not committed)
├── .env.example       # Template
├── .gitignore         # Git ignore rules
├── README_PYTHON.md   # Full documentation
└── QUICKSTART.md      # 5-min setup guide
```

## Old Files (Can Delete)
- `server.js`, `package.json`, `tsconfig.json` - Failed TypeScript attempts
- `app/`, `lib/`, `node_modules/`, `.next/` - Next.js leftovers
- `bot.log` - Old logs

## Next Steps
1. **Fix website**: Debug why deanna2u.com doesn't show ministores
2. **Push to GitHub**: Add remote and push
3. **Clean up**: Delete TypeScript files
4. **Test**: Create ministore and verify it appears on site

## Tech Stack
- Python 3.13
- python-telegram-bot 21.7
- OpenAI GPT-4o-mini
- SerperDev API (Google Shopping)
- MySQL 8.x on AWS RDS
- Long polling (no webhooks)

## Commands
```bash
# Run bot
python bot.py

# Stop bot
pkill -9 -f "python.*bot.py"

# Check status
ps aux | grep bot.py

# View commits
git log --oneline
```

## Database
- **User**: Sofia (ID 237)
- **Tables**: cliperest_book, cliperest_clipping
- **Host**: AWS RDS (snaps2u.cniamgkwcmgr.us-east-1.rds.amazonaws.com)

## Current State
Bot is WORKING and CREATING ministores. Website display is the only remaining issue.
