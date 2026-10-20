import requests
from aiogram import Bot, Dispatcher, executor, types

# Token va URL'ni to'g'ridan-to'g'ri shu yerga yozib qo'yamiz (Secret plan shart emas)
BOT_TOKEN = "8639262285:AAEhsBm1ncHtK180UqF_xDMYWdR5eSztivw"
OMNIROUTE_URL = (
    "https://omniroute-xxxx.onrender.com"  # Render bergan havolangiz
)

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

  headers = {"Content-Type": "application/json"}

  payload = {
      "model": "gpt-4o-mini",  # O'zingizga kerakli model
      "messages": [{"role": "user", "content": user_text}],
  }

  try:
    response = requests.post(
        f"{OMNIROUTE_URL}/v1/chat/completions", json=payload, headers=headers
    )
    res_data = response.json()

    answer = res_data["choices"][0]["message"]["content"]
    await message.answer(answer)
  except Exception as e:
    await message.answer(
        f"Xatolik yuz berdi. OmniRoute javob bera olmadi.\nXato: {e}"
    )


if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=True)
  
