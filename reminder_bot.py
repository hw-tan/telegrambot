import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am a test bot. Try these commands:\n'
                                  '/ping - I will respond with "pong"\n'
                                  '/echo [text] - I will repeat your text\n'
                                  '/status - I will tell you if I am working')

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send 'pong' when the command /ping is issued."""
    await update.message.reply_text('pong')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(f"You said: {update.message.text}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send status message."""
    await update.message.reply_text('✅ Bot is online and working!')

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
