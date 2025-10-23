from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

# --- Твой токен (замени на свой из BotFather) ---
TOKEN = "u"

# --- Список советов ---
eco_tips = [
    "Используй многоразовую бутылку вместо пластиковой 💧",
    "Выключай свет, когда выходишь из комнаты 💡",
    "Сдавай батарейки и лампочки в специальные контейнеры 🔋",
    "Сортируй мусор: пластик, стекло, бумага ♻️",
    "Бери с собой тканевую сумку в магазин 🛍️"
]

# --- Команда /start ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! 🌱 Я твой ЭкоБот.\n"
        "Я подскажу, как беречь природу!\n\n"
        "Напиши /sovet чтобы получить экологичный совет."
    )

# --- Команда /sovet ---
def sovet(update: Update, context: CallbackContext):
    tip = random.choice(eco_tips)
    update.message.reply_text("💡 Совет:\n" + tip)

# --- Основная функция ---
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sovet", sovet))

    print("Бот запущен... Нажми Ctrl+C для остановки.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()




