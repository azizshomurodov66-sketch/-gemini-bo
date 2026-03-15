import os
from flask import Flask
from threading import Thread
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

GEMINI_KEY = os.getenv("GEMINI_KEY")
TOKEN = os.getenv("BOT_TOKEN")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Salom! Men Gemini AI botman. Savol yozing yoki rasm yuboring.")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    image_data = await bot.download_file_by_id(photo.file_id)
    img = {"mime_type": "image/jpeg", "data": image_data.getvalue()}
    response = model.generate_content(["Ushbu rasmda nima bor? Yechib ber.", img])
    await message.reply(response.text)

@dp.message_handler()
async def handle_text(message: types.Message):
    response = model.generate_content(message.text)
    await message.answer(response.text)

if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
