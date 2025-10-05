import telebot
import threading
import time

TOKEN = ""  # <- вставь свой токен
bot = telebot.TeleBot(TOKEN)

# Словарь активных чатов {user_id: partner_id}
users = {}
# Пользователь, который ждёт собеседника
waiting_user = None

def notify_waiting(user_id):
    """Сообщение каждые 5 секунд пока пользователь ждёт"""
    global waiting_user
    count = 0
    while waiting_user == user_id:
        count += 1
        bot.send_message(user_id, f"Ищу собеседника... ({count*5} секунд)")
        time.sleep(5)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Используй /find чтобы найти собеседника, /stop чтобы выйти из чата.")

# /find
@bot.message_handler(commands=['find'])
def find(message):
    global waiting_user
    user_id = message.chat.id

    if user_id in users:
        bot.send_message(user_id, "Ты уже в чате. Напиши /stop, чтобы выйти.")
        return

    if waiting_user is None:
        waiting_user = user_id
        bot.send_message(user_id, "Ищу собеседника...")
        threading.Thread(target=notify_waiting, args=(user_id,), daemon=True).start()
    else:
        partner_id = waiting_user
        waiting_user = None
        users[user_id] = partner_id
        users[partner_id] = user_id
        bot.send_message(user_id, "Собеседник найден! Можете писать сообщения.")
        bot.send_message(partner_id, "Собеседник найден! Можете писать сообщения.")

# /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    global waiting_user
    user_id = message.chat.id

    # Если в чате
    if user_id in users:
        partner_id = users[user_id]
        bot.send_message(user_id, "Вы вышли из чата.")
        bot.send_message(partner_id, "Собеседник вышел из чата.")
        del users[user_id]
        del users[partner_id]
        return

    # Если ждёт собеседника
    if waiting_user == user_id:
        waiting_user = None
        bot.send_message(user_id, "Ты отменил поиск собеседника.")
        return

    bot.send_message(user_id, "Вы не ищете собеседника и не в чате. Используй /find.")

# Пересылка сообщений
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'sticker', 'audio', 'voice'])
def forward_message(message):
    user_id = message.chat.id
    if user_id in users:
        partner_id = users[user_id]
        bot.copy_message(partner_id, user_id, message.message_id)
    else:
        bot.send_message(user_id, "Вы не в чате. Используй /find чтобы начать поиск.")

# Запуск бота
bot.infinity_polling()
