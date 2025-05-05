import os
import asyncio
import schedule
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler
import google.generativeai as genai

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Настройка API ключей
os.environ["GOOGLE_API_KEY"] = "AIzaSyAAyat3z2cg76y4MIJYyH1ejmyyo5Vn7kE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
TELEGRAM_TOKEN = "7756361019:AAFxObOlgZzXvDDZIRPPiAEETHv3qTT3LE0"

# Инициализация Telegram бота
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Функция для генерации текста с помощью google-generativeai
async def generate_post_text():
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = (
            "Сгенерируй текст для поста в Telegram. "
            "Текст должен быть грамотным, легко читаемым и интересным для аудитории. "
            "Добавь релевантную информацию, факт или короткую историю. "
            "Используй абзацы или эмодзи для улучшения форматирования и вовлечения. "
            "Закончи призывом к действию или вопросом, чтобы стимулировать комментарии "
            '(например, "Что вы думаете?", "Поделитесь своим мнением"). '
            "Длина текста должна быть оптимальной для чтения в ленте Telegram (не слишком длинной). "
            "Избегай опечаток и грамматических ошибок."
        )
        response = model.generate_content(prompt)
        logging.info("Текст поста успешно сгенерирован.")
        return response.text
    except Exception as e:
        logging.error(f"Ошибка генерации текста: {str(e)}")
        return f"Ошибка генерации текста: {str(e)}"

# Асинхронная функция для отправки поста в канал
async def post_to_channel():
    try:
        bot = Bot(TELEGRAM_TOKEN)
        text = await generate_post_text()
        await bot.send_message(
            chat_id="@Биохакинг",
            text=text
        )
        logging.info("Пост успешно опубликован в канал @Биохакинг.")
    except Exception as e:
        logging.error(f"Ошибка при публикации поста: {str(e)}")

# Асинхронная команда /start для проверки бота
async def start(update, context):
    await update.message.reply_text("Бот запущен! Я буду публиковать посты в канал каждые 30 минут.")

# Добавляем команду в бота
app.add_handler(CommandHandler("start", start))

# Функция для настройки расписания
def schedule_posts():
    schedule.every(30).minutes.do(lambda: asyncio.create_task(post_to_channel()))

# Асинхронная функция для запуска расписания
async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

# Основная функция
async def main():
    logging.info("Запуск бота...")
    schedule_posts()
    await asyncio.gather(
        app.run_polling(),
        run_schedule()
    )

if __name__ == "__main__":
    asyncio.run(main())
