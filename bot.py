import os
import requests
from aiogram import Bot, Dispatcher, executor, types

# Token va URL ma'lumotlari Render'dagi Environment Variables'dan olinadi
BOT_TOKEN = os.getenv("BOT_TOKEN")
OMNIROUTE_URL = os.getenv("OMNIROUTE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
  await message.reply(
      "Salom! Men OmniRoute orqali ishlaydigan AI botman. Menga savolingizni"
      " yozing!"
  )


@dp.message_handler()
async def handle_message(message: types.Message):
  user_text = message.text

  # OmniRoute'ga so'rov yuborish uchun ma'lumotlar
  headers = {"Content-Type": "application/json"}

  payload = {
      "model": "gpt-4o-mini",  # O'zingiz xohlagan model nomini yozishingiz mumkin (masalan: deepseek-chat, gpt-4o-mini va h.k.)
      "messages": [{"role": "user", "content": user_text}],
  }

  try:
    # Render'dagi OmniRoute manziliga so'rov yuboramiz
    response = requests.post(
        f"{OMNIROUTE_URL}/v1/chat/completions", json=payload, headers=headers
    )
    res_data = response.json()

    # Kelgan javobni ajratib olib, botga chiqaramiz
    answer = res_data["choices"][0]["message"]["content"]
    await message.answer(answer)
  except Exception as e:
    await message.answer(
        f"Xatolik yuz berdi. OmniRoute javob bera olmadi.\nXato: {e}"
    )


if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=True)
