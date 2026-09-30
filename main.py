import os
import time
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

# Беремо токен із змінних оточення (Environment Variables) для безпеки
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8685969464:AAEru3z-hKVeygK5W0GG7ilXmF7TdAYOBOQ")

MORNING_MESSAGE = """🌞 Як прокидаєшся, роби зарядку.💪 
Приймай прохолодну воду ззовні, теплу внутрішньо 🌈

Ти барабанщик, музикант. Сьогодні ти мусиш позайматися музикою, а саме барабанами🥁
Повчи англійську💬

Як завжди, створюй своє 🌠"""

bot = telebot.TeleBot(BOT_TOKEN)
USER_ID = os.environ.get("USER_ID")  # Будемо зберігати твій ID прямо на сервері


@bot.message_handler(commands=["start"])
def send_welcome(message):
    global USER_ID
    USER_ID = message.chat.id
    print(f"Запам'ятали USER_ID: {USER_ID}")
    bot.reply_to(
        message,
        "Привіт! Я твій особистий ранковий помічник 🥁\n"
        "Я завантажений на хмарний сервер Render і надсилатиму тобі натхнення щоранку о 08:00!\n\n"
        "Напиши /morning, щоб перевірити повідомлення зараз.",
    )


@bot.message_handler(commands=["morning"])
def send_morning_manual(message):
    bot.send_message(message.chat.id, MORNING_MESSAGE)


def send_morning_reminder():
    if USER_ID:
        try:
            bot.send_message(USER_ID, MORNING_MESSAGE)
            print("Ранкове повідомлення успішно надіслано!")
        except Exception as e:
            print(f"Помилка відправки: {e}")
    else:
        print("Помилка: USER_ID ще не встановлено. Напишіть боту /start!")


if __name__ == "__main__":
    scheduler = BackgroundScheduler(timezone="Europe/Kyiv")
    scheduler.add_job(send_morning_reminder, "cron", hour=8, minute=0)
    scheduler.start()

    print("Бот успішно запущений на сервері Render!")
    bot.infinity_polling(skip_pending=True)
