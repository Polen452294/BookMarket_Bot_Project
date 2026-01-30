from aiogram.fsm.state import StatesGroup, State

class OrderFlow(StatesGroup):
    text = State()
    phone = State()

class AdminComment(StatesGroup):
    text = State()
