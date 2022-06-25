from aiogram import types, Dispatcher


async def echo(message: types.Message):
    await message.answer(message.text)

def setup(dp: Dispatcher):
    dp.register_message_handler(echo)
