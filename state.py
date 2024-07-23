import bcrypt
from aiogram.fsm.state import StatesGroup, State


class FormStudent(StatesGroup):
    first_name = State()
    last_name = State()
    group = State()
    confirm = State()


class GroupForm(StatesGroup):
    name = State()


class UpdateBall(StatesGroup):
    pass

