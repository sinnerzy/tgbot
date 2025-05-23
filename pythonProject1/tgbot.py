import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7552287228:AAEraRX3wL5ijYrSfauwai_g6KL3irY29b0'
WEATHER_API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

notes = []

# Клавиатура с кнопками
main_keyboard = [
    ["Погода", "Шутка", "Котик"],
    ["Добавить заметку", "Просмотреть заметки"],
    ["Инфо", "Подписаться"]
]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Выберите действие из меню ниже:",
        reply_markup=markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Погода":
        await update.message.reply_text("Напишите город командой /weather <название города>", reply_markup=ReplyKeyboardRemove())
    elif text == "Шутка":
        await joke(update, context)
    elif text == "Котик":
        await cat(update, context)
    elif text == "Добавить заметку":
        await update.message.reply_text("Введите заметку командой /note <текст заметки>", reply_markup=ReplyKeyboardRemove())
    elif text == "Просмотреть заметки":
        await view_notes(update, context)
    elif text == "Инфо":
        await info(update, context)
    elif text == "Подписаться":
        await subscribe(update, context)
    else:
        await update.message.reply_text("Команда не распознана. Попробуйте снова.")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = ' '.join(context.args)
    if not city:
        await update.message.reply_text('Пожалуйста, укажите название города.')
        return
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        weather_info = f"Погода в {data['name']}:\nТемпература: {data['main']['temp']}°C\n{data['weather'][0]['description']}"
        await update.message.reply_text(weather_info)
    except requests.exceptions.HTTPError as http_err:
        await update.message.reply_text(f'HTTP ошибка: {http_err}')
    except Exception as err:
        await update.message.reply_text(f'Ошибка: {err}')

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get('https://v2.jokeapi.dev/joke/Any')
    if response.status_code == 200:
        joke_data = response.json()
        if joke_data['type'] == 'single':
            await update.message.reply_text(joke_data['joke'])
        else:
            await update.message.reply_text(f"{joke_data['setup']}\n{joke_data['delivery']}")
    else:
        await update.message.reply_text('Не удалось получить шутку. Попробуйте позже.')

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    if response.status_code == 200:
        cat_data = response.json()
        await update.message.reply_photo(cat_data[0]['url'])
    else:
        await update.message.reply_text('Не удалось получить изображение котика. Попробуйте позже.')

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    note_text = ' '.join(context.args)
    if note_text:
        notes.append(note_text)
        await update.message.reply_text('Заметка сохранена!')
    else:
        await update.message.reply_text('Пожалуйста, введите текст заметки.')

async def view_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if notes:
        await update.message.reply_text('\n'.join(notes))
    else:
        await update.message.reply_text('Заметок нет.')

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Я бот sinnerzy, созданный для учебной практики. Версия 1.0')

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Вы подписаны на новости!')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("cat", cat))
    application.add_handler(CommandHandler("note", note))
    application.add_handler(CommandHandler("view_notes", view_notes))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    application.run_polling()

if __name__ == '__main__':
    main()
