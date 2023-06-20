from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import welcome, age_image_handler, attractiveness_image_handler, question_answer, question_answer_tochno
from bot.states import States

TOKEN = open('token/token.txt').read() ## paste path to txt file with bot's token

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.register_message_handler(welcome, commands=["start"], state="*")
dp.register_message_handler(age_image_handler, state=States.image_age, content_types="photo")
dp.register_message_handler(attractiveness_image_handler, state=States.image_attractiveness, content_types="photo")
dp.register_message_handler(question_answer, state=States.work)
dp.register_message_handler(question_answer_tochno, state=States.question)

if __name__ == "__main__":
    executor.start_polling(dp)
