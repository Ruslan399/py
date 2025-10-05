import telebot
import threading
import time

TOKEN = ""  # вставь сюда токен своего бота
bot = telebot.TeleBot(TOKEN)

# Активные чаты {user_id: partner_id}
users = {}
# Пользователь, ожидающий собеседника
waiting_user = None

def notify_waiting(user_id):
    """Отправляет уведомление каждые 5 секунд, пока пользователь ждёт"""
    global waiting_user
    count = 0
    while waiting_user == user_id:
        count += 1
        try:
            bot.send_message(user_id, f"Ищу собеседника... ({count*5} секунд прошло)")
        except:
            break
        time.sleep(5)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Это анонимный чат-бот.\n\n"
        "Используй команды:\n"
        "• /find — начать поиск собеседника\n"
        "• /stop — выйти из чата\n"
        "• /help — показать все команды"
    )

# /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "🧭 Список доступных команд:\n\n"
        "✅ /start — перезапустить бота\n"
        "🔍 /find — найти случайного собеседника\n"
        "⛔ /stop — завершить диалог\n"
        "ℹ️ /help — показать это сообщение"
    )

# /find
@bot.message_handler(commands=['find'])
def find(message):
    global waiting_user
    user_id = message.chat.id

    if user_id in users:
        bot.send_message(user_id, "⚠️ Ты уже общаешься. Используй /stop, чтобы выйти.")
        return

    if waiting_user == user_id:
        bot.send_message(user_id, "Ты уже ищешь собеседника, пожалуйста подожди ⏳")
        return

    if waiting_user is None:
        waiting_user = user_id
        bot.send_message(user_id, "🔎 Ищу собеседника...")
        threading.Thread(target=notify_waiting, args=(user_id,), daemon=True).start()
    else:
        partner_id = waiting_user
        waiting_user = None
        users[user_id] = partner_id
        users[partner_id] = user_id
        bot.send_message(user_id, "🎉 Собеседник найден! Можешь писать.")
        bot.send_message(partner_id, "🎉 Собеседник найден! Можешь писать.")

# /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    global waiting_user
    user_id = message.chat.id

    if user_id in users:
        partner_id = users[user_id]
        bot.send_message(user_id, "❌ Ты вышел из чата.")
        bot.send_message(partner_id, "⚠️ Собеседник покинул чат.")
        del users[user_id]
        del users[partner_id]
        return

    if waiting_user == user_id:
        waiting_user = None
        bot.send_message(user_id, "🚫 Поиск собеседника отменён.")
        return

    bot.send_message(user_id, "Ты не в чате. Используй /find, чтобы начать поиск.")

# Пересылка сообщений
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'sticker', 'audio', 'voice'])
def forward_message(message):
    user_id = message.chat.id
    if user_id in users:
        partner_id = users[user_id]
        bot.copy_message(partner_id, user_id, message.message_id)
    else:
        bot.send_message(user_id, "Ты не в чате. Напиши /find, чтобы найти собеседника.")

# Запуск бота
print("✅ Бот запущен и готов к работе!")
bot.infinity_polling()


