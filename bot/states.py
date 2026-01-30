from aiogram.fsm.state import State, StatesGroup


class OrderFlow(StatesGroup):
    text = State()
    phone = State()