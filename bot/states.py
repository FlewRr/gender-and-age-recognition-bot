from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    work = State()
    question = State()
    image_age = State()
    image_attractiveness = State()
    face_detection = State()