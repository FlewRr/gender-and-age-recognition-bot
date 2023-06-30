from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import welcome, age_image_handler, attractiveness_image_handler, face_detection_handler, question_answer, question_answer_tochno
from bot.states import States
from create_bot import bot

dp = Dispatcher(bot, storage=MemoryStorage())

dp.register_message_handler(welcome, commands=["start"], state="*")
dp.register_message_handler(age_image_handler, state=States.image_age, content_types="photo")
dp.register_message_handler(attractiveness_image_handler, state=States.image_attractiveness, content_types="photo")
dp.register_message_handler(face_detection_handler, state=States.face_detection, content_types="photo")
dp.register_message_handler(question_answer, state=States.work)
dp.register_message_handler(question_answer_tochno, state=States.question)


if __name__ == "__main__":
    executor.start_polling(dp)
