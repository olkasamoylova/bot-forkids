import random
import telebot
import datetime
import time
import threading

bot = telebot.TeleBot("здесь будет ваш токен")

# задаем переменные, что в нашей задумке нужны
notes = []

schedule = {
    "08:00": "Подъем",
    "08:15": "Умывание",
    "09:30": "Завтрак",
    "12:30": "Обед",
    "14:30": "Дневной отдых",
    "16:10": "Перекус",
    "18:30": "Ужин",
    "20:30": "Сказка на ночь"
}

games = [
    ("Игра: Запомни и найди - развивает память и концентрацию. Инструкция: Разложите перед ребёнком несколько предметов. Пусть он их запомнит, а когда он закроет глаза, то уберите один предмет. Задача ребёнка — найти, какой предмет исчез."),
    ("Игра: Конструктор - развивает мелкую моторику и воображение. Инструкция: Постройте вместе с ребёнком какую-то простую конструкцию из кубиков или конструктора. Обсудите, что получилось и как можно улучшить. Дайте ребёнку возможность поэкспериментировать с формами и размерами."),
    ("Игра: Придумай сказку - развивает речь и воображение. Инструкция: Начните рассказывать короткую сказку, но остановитесь на самом интересном месте и предложите ребёнку придумать продолжение. Поддерживайте его фантазию вопросами и добавляйте детали."),
    ("Игра: Рисование пальчиками - развивает мелкую моторику и творческое мышление. Инструкция: Возьмите краски и предложите ребёнку рисовать пальцами. Можно изобразить небо, деревья, животных и т.д. Дайте ребёнку свободу выражать себя через рисунок."),
    ("Игра в слова - развивает словарный запас и речевые навыки. Инструкция: Начните игру с простого слова, а ребёнок должен придумать слово, начинающееся на последнюю букву вашего слова. Продолжайте по очереди, пока не закончится время или не сложатся новые слова.")
]

# создаем команды, которые работают в чат-боте

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message,
        "Привет! Я бот для напоминания о распорядке дня ребёнка.\n"
        "Я могу:\n"
        "- Напоминать о ключевых моментах дня\n"
        "- Показывать расписание на остаток дня (/help)\n"
        "- Предлагать полезные игры для развития (/game)\n"
        "- Вести заметки о ребёнке (/note и /notes)\n"
    )
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start() # поток напоминалок работает всегда

@bot.message_handler(commands=['help'])
def help_message(message):
    now = datetime.datetime.now().strftime("%H:%M")
    remaining_schedule = [f"{time} - {activity}" for time, activity in schedule.items() if time > now]

    if remaining_schedule:
        bot.reply_to(message, "Расписание на остаток дня:\n" + "\n".join(remaining_schedule))
    else:
        bot.reply_to(message, "На сегодня расписание выполнено!")

@bot.message_handler(commands=['game'])
def game_message(message):
    game = random.choice(games)
    bot.reply_to(message,game)

@bot.message_handler(commands=['note'])
def add_note_message(message):
    msg = bot.reply_to(message, "Введите вашу заметку о ребёнке:")
    bot.register_next_step_handler(msg, save_note)

def save_note(message):
    note = {
        'text': message.text,
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    notes.append(note)
    bot.reply_to(message, "Заметка сохранена!")

@bot.message_handler(commands=['notes'])
def notes_message(message):
    if notes:
        notes_text = "\n".join([f"{note['time']} - {note['text']}" for note in notes])
        bot.reply_to(message, "Ваши заметки:\n" + notes_text)
    else:
        bot.reply_to(message, "У вас пока нет заметок.")

# создаем напоминалки
def send_reminders(chat_id):
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in schedule:
            bot.send_message(chat_id, f"Напоминание: {schedule[now]}")
            time.sleep(61)  # Предотвращаем повторную отправку напоминания в ту же минуту
        time.sleep(1)

bot.polling(non_stop=True)
