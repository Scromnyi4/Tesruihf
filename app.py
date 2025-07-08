import requests
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler

app = Flask(__name__)

# Конфигурация
BOT_TOKEN = "7351570614:AAGhSHkNxKpzw0NPFabCXrSdkL0wNYpNl2o"  # Замените на ваш токен
RENDER_URL = "https://hostingbot990.onrender.com/"  # Ваш URL на Render
PING_INTERVAL = 100  # 2 минут (минимальный интервал для бесплатного плана)

@app.route('/')
def home():
    return "🟢 Бот активен и работает нормально!"

def keep_alive():
    """Функция для автоматического пинга"""
    while True:
        try:
            requests.get(RENDER_URL)
            print(f"[Пинг] Отправлен запрос в {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[Ошибка] Пинг не удался: {e}")
        time.sleep(PING_INTERVAL)

async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("🚀 Бот работает исправно!")

def run_flask():
    """Запуск Flask сервера"""
    app.run(host='0.0.0.0', port=8080)

def main():
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Запускаем авто-пинг в отдельном потоке
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Настройка Telegram бота
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("🤖 Бот успешно запущен с авто-пингом!")
    application.run_polling()

if __name__ == "__main__":
    import time
    main()
