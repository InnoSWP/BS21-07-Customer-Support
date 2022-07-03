import logging
import sqlite3
import requests

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode
from aiogram.utils import executor

conUser = sqlite3.connect('users.db')
curUser = conUser.cursor()
conInstance = sqlite3.connect('instances.db')
curInstance = conInstance.cursor()
conBusy = sqlite3.connect('busies.db')
curBusy = conBusy.cursor()
bot_id = 5389656216
API_TOKEN = '5505131588:AAF_LojeoLfIAlhd6UJnV36gDS-yDZei9Nw'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    name = State()
    surname = State()


class Request(StatesGroup):
    answer = State()


class Client(StatesGroup):
    answer = State()


########### USER ###########


def deleteUser(id):
    print("DELETE USER")
    global conUser, curUser
    curUser.execute(f"DELETE FROM user WHERE id={id}")
    conUser.commit()


def addUser(id, name, surname):
    print("ADD USER")
    global conUser, curUser
    curUser.execute(f"INSERT INTO user VALUES ({id}, '{name}', '{surname}', 'user')")
    conUser.commit()


def findUser(id):
    global conUser, curUser
    result = list(curUser.execute(f"SELECT * FROM user WHERE id={id}"))
    if len(result) > 0:
        return True
    else:
        return False


def getUserName(id):
    global conUser, curUser
    result = list(curUser.execute(f"SELECT * FROM user WHERE id={id}"))
    try:
        return result[-1][1]
    except:
        return ""


def getUserSurname(id):
    global conUser, curUser
    result = list(curUser.execute(f"SELECT * FROM user WHERE id={id}"))
    try:
        return result[-1][2]
    except:
        return ""


def getUserRole(id):
    global conUser, curUser
    result = list(curUser.execute(f"SELECT * FROM user WHERE id={id}"))
    try:
        return result[-1][3]
    except:
        return ""


def getUsers():
    global conUser, curUser
    result = list(curUser.execute(f"SELECT * FROM user"))
    return result


########### USER ###########


########### INSTANCE ###########


def deleteInstance(number):
    global conInstance, curInstance
    curInstance.execute(f"DELETE FROM instance WHERE number={number}")
    conInstance.commit()


def addInstance(number, id):
    global conInstance, curInstance
    curInstance.execute(f"INSERT INTO instance VALUES ({number}, {id}, 'Open')")
    conInstance.commit()


def findInstance(number):
    global conInstance, curInstance
    result = list(curInstance.execute(f"SELECT * FROM instance WHERE number={number}"))
    if len(result) > 0:
        return True
    else:
        return False


def getInstanceId(number):
    global conInstance, curInstance
    result = list(curInstance.execute(f"SELECT * FROM instance WHERE number={number}"))
    try:
        return result[-1][1]
    except:
        return ""


def getInstanceStatus(number):
    global conInstance, curInstance
    result = list(curInstance.execute(f"SELECT * FROM instance WHERE number={number}"))
    try:
        return result[-1][2]
    except:
        return ""


def getInstances():
    global conInstance, curInstance
    result = list(curInstance.execute(f"SELECT * FROM instance"))
    return result


########### INSTANCE ###########


########### BUSY ###########

def deleteBusy(id):
    print("DELETE BUSY")
    global conBusy, curBusy
    curBusy.execute(f"DELETE FROM busy WHERE id={id}")
    conBusy.commit()


def addBusy(id, number):
    print("ADD BUSY")
    global conBusy, curBusy
    curBusy.execute(f"INSERT INTO busy VALUES ({id}, {number})")
    conBusy.commit()


def findBusy(id):
    global conBusy, curBusy
    result = list(curBusy.execute(f"SELECT * FROM busy WHERE id={id}"))
    if len(result) > 0:
        return True
    else:
        return False


def getBusyNumber(id):
    global conBusy, curBusy
    result = list(curBusy.execute(f"SELECT * FROM busy WHERE id={id}"))
    try:
        return result[-1][1]
    except:
        return ""


def getBusies(id):
    global conBusy, curBusy
    result = list(curBusy.execute(f"SELECT * FROM busy"))
    return result


########### BUSY ###########


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if findUser(message.chat.id):
        await message.answer(f"{getUserName(message.chat.id)}, welcome back!")
    else:
        await Form.name.set()
        await message.answer("Hello! Nice to meet you.\n\nIf you want join to our team, please, register in system.\nWrite your name.")

@dp.message_handler(commands=["delete_me"])
async def delete_me(message: types.Message):
    if findUser(message.chat.id):
        await message.answer(f"{getUserName(message.chat.id)}, your user successful deleted!")
        deleteUser(message.chat.id)
        deleteBusy(message.chat.id)
    else:
        await message.answer("You are not register yet!")

@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await message.answer("List of commands:\n"
                         "    /start - If you not register yet, you can register in system.\n"
                         "    /delete_me - You can delete your user from system.\n")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('ОК')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.answer(f"{message.text}, thanks. Write you surname.")


@dp.message_handler(state=Form.surname)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    async with state.proxy() as data:
        addUser(id=message.chat.id, name=data["name"], surname=data["surname"])
        addBusy(message.chat.id, 0)
    await message.answer(f"Thanks. You're registered in the system.")
    await state.finish()


@dp.message_handler(commands=["send_request"])
async def send_messages(message: types.Message):
    if getUserRole(message.chat.id) == "admin":
        await Request.answer.set()
        await message.answer("Write text of message:")
    else:
        await message.answer("You do not have enough permissions!")


@dp.message_handler(state=Request.answer)
async def text_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    async with state.proxy() as data:
        for i in getUsers():
            await bot.send_message(i[0], data['text'])
    await state.finish()
    await message.answer("Messages sent!")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('open'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    tmp = callback_query.data.split("===")
    number, text = int(tmp[1]), tmp[2]
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if findInstance(number):
        await bot.send_message(callback_query.from_user.id, "Request is busy!")
    else:
        await bot.answer_callback_query(callback_query.id)
        addInstance(number=number, id=callback_query.from_user.id)
        deleteBusy(callback_query.from_user.id)
        addBusy(id=callback_query.from_user.id, number=number)
        await bot.send_message(callback_query.from_user.id, text)
        await bot.send_message(bot_id, f"{number}==={getUserName(callback_query.from_user.id)} connected to the chat!")
        requests.get(f"http://127.0.0.1:5000/send/{number}/{getUserName(callback_query.from_user.id)} connected to the chat!")

async def send_all_request(number, text):
    if findInstance(number):
        if text == "close":
            deleteBusy(getInstanceId(number))
            addBusy(getInstanceId(number), 0)
            await bot.send_message(getInstanceId(number), "Request closed!")
            deleteInstance(number)
        else:
            await bot.send_message(getInstanceId(number), text)
    else:
        inline_btn_1 = InlineKeyboardButton('Start', callback_data=f'open==={number}==={text}')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
        for i in getUsers():
            if i[3] == "user" and getBusyNumber(int(i[0])) == 0:
                await bot.send_message(i[0], f"New request № {number}", reply_markup=inline_kb1)


@dp.message_handler()
async def new_request(message: types.Message):
    if getUserRole(message.chat.id) == "admin":
        number = message.text.split('===')[0]
        text = message.text.split('===')[1]
        await send_all_request(int(number), text)
    elif getBusyNumber(message.chat.id) != 0:
        await bot.send_message(bot_id, str(getBusyNumber(message.chat.id)) + "===" + message.text)
        requests.get(f"http://127.0.0.1:5000/send/{getBusyNumber(message.chat.id)}/{message.text}")


def start_bot():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    start_bot()
