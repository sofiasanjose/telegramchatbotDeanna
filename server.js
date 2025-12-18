import express from 'express';
import { Bot } from 'grammy';
import OpenAI from 'openai';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
app.use(express.json());

const userConversations = new Map();

function getUserSession(userId) {
  if (!userConversations.has(userId)) {
    userConversations.set(userId, { conversation: [], lastActivity: Date.now() });
  }
  const session = userConversations.get(userId);
  session.lastActivity = Date.now();
  return session;
}

const DEANNA_SYSTEM_PROMPT = `You are Deanna, an AI personal shopper and lifestyle curator. You talk like you're texting a close friend — super casual, warm, and real.

🎯 RULES:
- Text like a friend: short, natural, conversational AF
- 1-3 sentences MAX
- NO essays. NO lists. NO over-explaining.
- Emojis: 1-2 per message max (😊✨🙌💚)
- Ask quick follow-ups instead of dumping info
- Sound human, not robotic`;

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const bot = new Bot(process.env.TELEGRAM_BOT_TOKEN);

bot.command('start', async (ctx) => {
  const userId = ctx.from?.id;
  if (!userId) return;
  
  const session = getUserSession(userId);
  session.conversation = [];
  
  await ctx.reply("Hi! I'm Deanna — your AI personal shopper and lifestyle buddy. What's up? 💚 What can I help you find today?");
});

bot.command('clear', async (ctx) => {
  const userId = ctx.from?.id;
  if (!userId) return;
  
  const session = getUserSession(userId);
  session.conversation = [];
  
  await ctx.reply("✨ Memory cleared! Let's start fresh. What can I help you with?");
});

bot.on('message:text', async (ctx) => {
  const userMessage = ctx.message.text;
  const userId = ctx.from?.id;
  if (!userId) return;

  const session = getUserSession(userId);
  session.conversation.push({ role: 'user', content: userMessage });

  if (session.conversation.length > 10) {
    session.conversation = session.conversation.slice(-10);
  }

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: DEANNA_SYSTEM_PROMPT },
        ...session.conversation,
      ],
      max_tokens: 50,
      temperature: 0.9,
    });

    const deannaResponse = response.choices[0].message.content || 'Hey! 💚';
    session.conversation.push({ role: 'assistant', content: deannaResponse });
    await ctx.reply(deannaResponse);
  } catch (error) {
    console.error('OpenAI Error:', error);
    await ctx.reply("Oops, I'm having a moment! Try again? 🙏");
  }
});

bot.catch((err) => console.error('Bot error:', err));

app.post('/webhook', async (req, res) => {
  try {
    await bot.handleUpdate(req.body);
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).send('Error');
  }
});

app.get('/', (req, res) => {
  res.send('Deanna bot is running! 💚');
});

const PORT = process.env.PORT || 3001;

(async () => {
  await bot.init();
  console.log('✅ Bot initialized');
  
  app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`🔗 Webhook ready at http://localhost:${PORT}/webhook`);
  });
})();
