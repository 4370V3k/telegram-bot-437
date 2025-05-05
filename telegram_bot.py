import os
import asyncio
import schedule
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler
import google.generativeai as genai

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

os.environ["GOOGLE_API_KEY"] = "AIzaSyAAyat3z2cg76y4MIJYyH1ejmyyo5Vn7kE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
TELEGRAM_TOKEN = "7756361019:AAFxObOlgZzXvDDZIRPPiAEETHv3qTT3LE0"

app = Application.builder().token(TELEGRAM_TOKEN).build()

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
            "Длина текста должна быть оптимальной для чтения в ленте Telegram. "
            "Избегай опечаток."
        )
        response = model.generate_content(prompt)
        logging.info("Текст поста успешно сгенерирован.")
        return response.text
    except Exception as e:
        logging.error(f"Ошибка генерации текста: {str(e)}")
        return f"Ошибка: {str(e)}"

async def post_to_channel():
    try:
        bot = Bot(TELEGRAM_TOKEN)
        text = await generate_post_text()
        await bot.send_message(chat_id="@Биохакинг", text=text)
        logging.info("Пост опубликован в @Биохакинг.")
    except Exception as e:
        logging.error(f"Ошибка при публикации: {str(e)}")

async def start(update, context):
    await update.message.reply_text("Бот запущен! Публикую посты каждые 30 минут.")

app.add_handler(CommandHandler("start", start))

def schedule_posts():
    schedule.every(30).minutes.do(lambda: asyncio.create_task(post_to_channel()))

async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

async def main():
    logging.info("Запуск бота...")
    schedule_posts()
    await asyncio.gather(app.run_polling(), run_schedule())

if __name__ == "__main__":
    asyncio.run(main())
