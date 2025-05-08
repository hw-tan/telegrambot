# Daily Reminder Telegram Bot

This is a Telegram bot that helps you set daily reminders. The bot will:
- Ask you at 9 AM what you want to be reminded of
- Send reminders every 2 hours until 6 PM
- Only send reminders if you've set one for the day

## Setup

1. Create a Telegram bot:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use the `/newbot` command to create a new bot
   - Copy the API token provided by BotFather

2. Create a `.env` file in the project directory with your bot token:
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```
   python reminder_bot.py
   ```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to begin
3. At 9 AM, the bot will ask what you want to be reminded of
4. Reply with your reminder text
5. The bot will send reminders every 2 hours until 6 PM

You can also manually trigger the reminder prompt by sending the `/remind` command. 