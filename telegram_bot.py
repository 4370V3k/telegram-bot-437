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
            "���������� ����� ��� ����� � Telegram. "
            "����� ������ ���� ���������, ����� �������� � ���������� ��� ���������. "
            "������ ����������� ����������, ���� ��� �������� �������. "
            "��������� ������ ��� ������ ��� ��������� �������������� � ����������. "
            "������� �������� � �������� ��� ��������, ����� ������������� ����������� "
            '(��������, "��� �� �������?", "���������� ����� �������"). '
            "����� ������ ������ ���� ����������� ��� ������ � ����� Telegram. "
            "������� ��������."
        )
        response = model.generate_content(prompt)
        logging.info("����� ����� ������� ������������.")
        return response.text
    except Exception as e:
        logging.error(f"������ ��������� ������: {str(e)}")
        return f"������: {str(e)}"

async def post_to_channel():
    try:
        bot = Bot(TELEGRAM_TOKEN)
        text = await generate_post_text()
        await bot.send_message(chat_id="@���������", text=text)
        logging.info("���� ����������� � @���������.")
    except Exception as e:
        logging.error(f"������ ��� ����������: {str(e)}")

async def start(update, context):
    await update.message.reply_text("��� �������! �������� ����� ������ 30 �����.")

app.add_handler(CommandHandler("start", start))

def schedule_posts():
    schedule.every(30).minutes.do(lambda: asyncio.create_task(post_to_channel()))

async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

async def main():
    logging.info("������ ����...")
    schedule_posts()
    await asyncio.gather(app.run_polling(), run_schedule())

if __name__ == "__main__":
    asyncio.run(main())
