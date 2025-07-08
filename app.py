import requests
import threading
import time
from flask import Flask
from telegram.ext import Application, CommandHandler

app = Flask(__name__)

# Configuration
BOT_TOKEN = "7351570614:AAGhSHkNxKpzw0NPFabCXrSdkL0wNYpNl2o"  # Replace with your actual token
RENDER_URL = "https://hostingbot990.onrender.com/"  # Your Render URL
PING_INTERVAL = 120  # 2 minutes (minimum interval for Render free tier)

@app.route('/')
def home():
    return "🟢 Bot is active and running normally!"

def keep_alive():
    """Function to automatically ping the app"""
    while True:
        try:
            response = requests.get(RENDER_URL)
            print(f"[Ping] Sent request at {time.strftime('%H:%M:%S')} - Status: {response.status_code}")
        except Exception as e:
            print(f"[Error] Ping failed: {e}")
        time.sleep(PING_INTERVAL)

async def start(update, context):
    """Handler for /start command"""
    await update.message.reply_text("🚀 Bot is working properly!")

def run_flask():
    """Run Flask server"""
    app.run(host='0.0.0.0', port=8080)

def main():
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start auto-ping in a separate thread
    ping_thread = threading.Thread(target=keep_alive)
    ping_thread.daemon = True
    ping_thread.start()
    
    # Set up Telegram bot
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("🤖 Bot successfully launched with auto-ping!")
    application.run_polling()

if __name__ == "__main__":
    main()
