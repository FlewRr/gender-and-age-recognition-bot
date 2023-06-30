import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import cv2


transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


## should rewrite at OpenCV (cv2) !!!!
def prepare_image(path):
    image = Image.open(path).convert('RGB')
    image.load()
    image = np.array(image)
    #image = cv2.resize(image, dsize=(224, 224))
    image = transform(image)

    return image


def prepare_image_for_detection(path):
    """
    Input : Path to the image
    Return :  Original and gray images for cascade detection
    """
    image = cv2.imread(path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image, gray_image


def form_reply_keyboard(buttons_info, one_time=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)

    for i in range(len(buttons_info)):
        print(buttons_info[i])
        keyboard.add(KeyboardButton(str(buttons_info[i])))

    return keyboard
