import telebot
import random

# --- Твой токен (замени на свой) ---
TOKEN = ""

bot = telebot.TeleBot(TOKEN)

# --- Список советов ---
eco_tips = [
    "Используй многоразовую бутылку вместо пластиковой 💧",
    "Выключай свет, когда выходишь из комнаты 💡",
    "Сдавай батарейки и лампочки в специальные контейнеры 🔋",
    "Сортируй мусор: пластик, стекло, бумага ♻️",
    "Бери с собой тканевую сумку в магазин 🛍️"
]

# --- Команда /start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! 🌱 Я твой ЭкоБот.\n"
        "Я подскажу, как беречь природу!\n\n"
        "Напиши /sovet чтобы получить экологичный совет."
    )

# --- Команда /sovet ---
@bot.message_handler(commands=['sovet'])
def sovet(message):
    tip = random.choice(eco_tips)
    bot.send_message(message.chat.id, "💡 Совет:\n" + tip)

# --- Если пользователь пишет что-то другое ---
@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "Напиши /sovet чтобы получить совет 🌿")

# --- Запуск ---
print("Бот запущен... Нажми Ctrl+C для остановки.")
bot.polling(none_stop=True)



