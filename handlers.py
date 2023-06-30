from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.input_file import InputFile
from aiogram.dispatcher import FSMContext
from utils import messages, utils
from model.predictor import model_age, model_beaty
from detector.detector import face_cascade
from bot.states import States
import torch
import os
import cv2
from create_bot import bot

async def welcome(msg: types.Message):
    await States.work.set()
    await msg.reply(messages.start, reply_markup=utils.form_reply_keyboard(["Let's start that shit", "Nah, I'll pass"]))
    

async def age_image_handler(msg: types.Message, state: FSMContext):
    images = msg.photo

    if images is None:
        await msg.reply("This is not a photo")
        return 0
    
    image = images[-1]
    path = f"images/{msg.from_user.id}.jpeg"

    await image.download(path)

    prediction = model_age(utils.prepare_image(path).unsqueeze(0))
    prediction = int(torch.argmax(prediction, 1))

    await msg.reply(messages.prediction.format(prediction+1))
    await welcome(msg)


async def attractiveness_image_handler(msg: types.Message, state: FSMContext):
    images = msg.photo

    if images is None:
        await msg.reply("This is not a photo")
        return 0

    image = images[-1]
    path = f"images/{msg.from_user.id}.jpeg"

    await image.download(path)

    prediction = model_beaty(utils.prepare_image(path).unsqueeze(0))
    prediction = int(torch.argmax(prediction, 1))
    
    await msg.reply(messages.prediction.format(prediction+1))
    await welcome(msg)


async def face_detection_handler(msg: types.Message, state: FSMContext):
    images = msg.photo

    if images is None:
        await msg.reply("This is not a photo")
        return 0
    
    image = images[-1]
    path = f"images/{msg.from_user.id}.jpeg"

    await image.download(path)

    detecting_image, gray_image = utils.prepare_image_for_detection(path)
    
    prediction = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    
    for (x, y, w, h) in prediction:
        cv2.rectangle(detecting_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    cv2.imwrite(path, detecting_image)
    
    photo = InputFile(path)

    await bot.send_photo(msg.from_user.id, photo)
    await msg.reply('That\'s it, hope you\'ll like it')
    await welcome(msg)

async def question_answer(msg: types.Message, state: FSMContext):
    await States.question.set()

    if msg.text == f"Nah, I\'ll pass":
        await msg.reply(messages.error)
        return 0
    else:
        await msg.reply(messages.question, reply_markup=utils.form_reply_keyboard(['Age', 'Gender', 'Hot or Not', 'Face Detection', 'I\'m out of here']))
    

async def question_answer_tochno(msg: types.Message, state: FSMContext):

    if msg.text == 'I\'m out of here':
        await msg.reply(messages.error)
        return 0
    elif msg.text == 'Age':
        await States.image_age.set()
        await msg.reply(messages.image_age)
    elif msg.text == 'Hot or Not':
        await States.image_attractiveness.set()
        await msg.reply(messages.image_hot)
    elif msg.text == 'Face Detection':
        await States.face_detection.set()
        await msg.reply(messages.image_detection)
    elif msg.text == 'Gender':
        await msg.reply("This is currently not available due to your geolocation")
        return 0
    else:
        await msg.reply("I did not understand this")
        return 0
    

