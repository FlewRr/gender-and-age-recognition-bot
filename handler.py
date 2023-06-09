from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from utils import messages, utils
from model.predictor import model
from bot.states import States
import torch


async def welcome(msg: types.Message):
    await States.work.set()
    await msg.reply(messages.start, reply_markup=utils.form_reply_keyboard(["Positive", "Negative"]))


async def image_handler(msg: types.Message, state: FSMContext):
    images = msg.photo

    if images is None:
        await msg.reply("This is not a photo")
        return 0
    
    image = images[-1]
    path = f"{msg.from_user.id}.jpeg"

    await image.download(path)

    prediction = model(utils.prepare_image(path).unsqueeze(0))
    prediction = int(torch.argmax(prediction, 1))

    await msg.reply(messages.prediction.format(prediction))
    await welcome(msg)


async def question_answer(msg: types.Message, state: FSMContext):
    await States.question.set()
    await msg.reply(messages.question, reply_markup=utils.form_reply_keyboard(['Yes']))


async def question_answer_tochno(msg: types.Message, state: FSMContext):
    await States.image.set()

    if msg.text != "Yes":
        await msg.reply(messages.error, reply_markup=utils.form_reply_keyboard(["Yes"]))
    else:
        await States.image.set()
        await msg.reply(messages.image)
    

