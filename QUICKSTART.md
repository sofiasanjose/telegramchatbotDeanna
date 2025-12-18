# Quick Start Guide

## Get Bot Running in 5 Minutes

### 1. Clone & Setup
```bash
cd /Users/sofiaclaudiabonoan/Desktop/deanna-ministore-system
source .venv/bin/activate
```

### 2. Install (if needed)
```bash
pip install -r requirements.txt
```

### 3. Run Bot
```bash
python bot.py
```

### 4. Test in Telegram
1. Open @DeannaChat_bot
2. Send: `/start`
3. Ask for product recommendations
4. Send: `/ministore`

## Stop Bot
```bash
pkill -9 -f "python.*bot.py"
```

## Check if Running
```bash
ps aux | grep bot.py
```

## View Logs
Bot prints to console. To run in background:
```bash
nohup python bot.py > bot.log 2>&1 &
```

## Common Issues

**"Bot not responding"**
```bash
pkill -9 -f "python.*bot.py"  # Kill old instance
sleep 2
python bot.py  # Start fresh
```

**"Module not found"**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**"Database error"**
Check `.env` file has correct DB credentials

## Files You Need

✅ Keep these:
- `bot.py` - Main bot
- `analyzer.py` - Product detector
- `ministore.py` - Store creator
- `requirements.txt` - Dependencies
- `.env` - Your API keys (DO NOT COMMIT)
- `.gitignore` - Git ignore rules

❌ Can delete (old TypeScript attempts):
- `server.js`
- `package.json`
- `tsconfig.json`
- `next.config.ts`
- `app/` folder
- `lib/` folder
- `node_modules/`
- `.next/`
