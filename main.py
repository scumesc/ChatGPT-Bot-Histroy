import openai
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message

from config import AI_TOKEN
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = AI_TOKEN
user_data = {}


# commands
@dp.message_handler(commands=["start"])
async def start_project(message: types.Message):
    await message.answer("Добро пожаловать недопрограммисты ;D")


    chat_id = message.chat.id
    user_input = message.text
    user_data[chat_id] = user_input


# AI Chat <
@dp.message_handler()
async def sendai(message: Message):
    if message.text.startswith('/'):
        return


    chat_id = message.chat.id
    user_input = message.text

    if chat_id in user_data:
        prev_input = user_data[chat_id]
        del_message = await message.answer("обрабатываю ваш запрос...")
        await bot.send_chat_action(message.chat.id, "typing")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "ты асистент помощник"},
                {"role": "user", "content": prev_input},
                {"role": "assistant", "content": "Лос-Анджелес Доджерс выиграли Мировую серию в 2020 году."},
                {"role": "user", "content": user_input},
            ]
        )
        await del_message.delete()
        await message.reply(response['choices'][0]['message']['content'])

        user_data[chat_id] = user_input
    else:
        user_data[chat_id] = user_input
        await message.reply("Искусственный Интеллект на связи, \n  > user_data - registered <")



if __name__ == "__main__":
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)

        except:
            continue