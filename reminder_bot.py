import os
import logging
from datetime import datetime, time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import schedule
import time as time_module
import threading

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Conversation states
WAITING_FOR_REMINDER = 1

# Store user reminders
user_reminders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi! I am your reminder bot. I will ask you at 9 AM what you want to be reminded of for the day.'
    )

async def ask_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask user what they want to be reminded of."""
    await update.message.reply_text(
        "What would you like to be reminded of today?"
    )
    return WAITING_FOR_REMINDER

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the reminder and confirm to the user."""
    user_id = update.effective_user.id
    reminder_text = update.message.text
    user_reminders[user_id] = reminder_text
    
    await update.message.reply_text(
        f"I'll remind you about: {reminder_text}\n"
        "I'll send reminders every 2 hours until 6 PM."
    )
    return ConversationHandler.END

async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send reminder to users."""
    current_time = datetime.now().time()
    if current_time >= time(18, 0):  # After 6 PM
        return

    for user_id, reminder in user_reminders.items():
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Reminder: {reminder}"
            )
        except Exception as e:
            logger.error(f"Failed to send reminder to user {user_id}: {e}")

def run_scheduler(application: Application):
    """Run the scheduler in a separate thread."""
    while True:
        schedule.run_pending()
        time_module.sleep(1)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('remind', ask_reminder)],
        states={
            WAITING_FOR_REMINDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_reminder)],
        },
        fallbacks=[],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    # Schedule reminders
    schedule.every().day.at("09:00").do(lambda: application.create_task(ask_reminder(None, None)))
    schedule.every(2).hours.do(lambda: application.create_task(send_reminder(None)))

    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, args=(application,))
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 