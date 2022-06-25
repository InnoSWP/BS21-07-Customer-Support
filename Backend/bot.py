import logging
from telethon import TelegramClient, sync, events
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.types import ParseMode
from aiogram.utils import executor
import databaseHandler

counter = databaseHandler.sheetRows()

api_id = 16961014
api_hash = '5a99188f19d18c44778b8eed6d49a3d5'

def send_message(message):
    client = TelegramClient('SWPbot', api_id, api_hash)
    client.start()
    client.send_message('@swp_g7_bs21_backend_bot', message)

bot_id = 742596099
API_TOKEN = '5465574210:AAHmn0cQlDJNSCROnbHnRLQ7JvixZofw4UQ'
logging.basicConfig(level=logging.INFO)



bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
database = {}
instance = {}
isBusy = {}


class Form(StatesGroup):
    name = State()
    surname = State()


class Request(StatesGroup):
    answer = State()


class Client(StatesGroup):
    answer = State()



def read_data(nameDatabase):
    global database
    file = open(nameDatabase)
    for i in file:
        print(i)
        id, name, surname, userType = i.split()
        database[int(id)] = {"Name": name, "Surname": surname, "Type": userType}
        isBusy[int(id)] = "0"
    file.close()


def delete_user(nameDatabase, id):
    global database
    database.pop(id)
    file = open(nameDatabase, "w")
    for i, j in database.items():
        print(i, j["Name"], j["Surname"], j["Type"], file=file)
    file.close()


def add_user(nameDatabase, id, name, surname):
    global database
    file = open(nameDatabase, "a")
    print(id, name, surname, "user", file=file)
    database[int(id)] = {"Name": name, "Surname": surname, "Type": "user"}
    isBusy[int(id)] = "0"
    file.close()



@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.chat.id in database:
        await message.answer(f"{database[message.chat.id]['Name']}, welcome back!")
    else:
        await Form.name.set()
        await message.answer(
            "Hello! Nice to meet you.\n\nIf you want join to our team, please, register in system.\nWrite your name.")


@dp.message_handler(commands=["delete_me"])
async def delete_me(message: types.Message):
    if message.chat.id in database:
        await message.answer(f"{database[message.chat.id]['Name']}, your user successful deleted!")
        delete_user("volunteers.txt", message.chat.id)
    else:
        await message.answer("You are not register yet!")


@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await message.answer("List of commands:\n"
                         "    /start - If you not register yet, you can register in system.\n"
                         "    /delete_me - You can delete your user from system.\n"
                         "    /link - Get link to the Google Sheets database ")


@dp.message_handler(commands=["link"])
async def send_welcome(message: types.Message):
    await message.answer("Google Sheets link:\n"
                         "https://docs.google.com/spreadsheets/d/1PwgkG6nqIQqj7KiXRv19Hcy0igg9EfS6kkG2gfVDgzI/edit#gid=0")


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
        database[message.chat.id] = {"Name": data["name"], "Surname": data["surname"]}
        add_user("volunteers.txt", id=message.chat.id, name=data["name"], surname=data["surname"])
    await message.answer(f"Thanks. You're registered in the system.")
    await state.finish()


@dp.message_handler(state=Form.surname)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    async with state.proxy() as data:
        database[message.chat.id] = {"Name": data["name"], "Surname": data["surname"]}
        add_user("volunteers.txt", id=message.chat.id, name=data["name"], surname=data["surname"])
    await message.answer(f"Thanks. You're registered in the system.")
    await state.finish()


@dp.message_handler(commands=["send_request"])
async def send_request(message: types.Message):
    if database[message.chat.id]["Type"] == "admin":
        await Request.answer.set()
        await message.answer("Write text of message:")
    else:
        await message.answer("You do not have enough permissions!")


@dp.message_handler(state=Request.answer)
async def text_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    global counter
    values = databaseHandler.sheetRead()
    sent = False
    for value in values:
        if value[0] == data['text'] and len(value) != 1:
            await bot.send_message(bot_id, value[1])
            sent = True
            break

    if not sent:
        databaseHandler.sheetWriteQuestion(counter, data['text'])
        async with state.proxy() as data:
            await send_all_request(counter, message.text)
        await state.finish()
        await message.answer("Messages sent!")
        counter += 1
    else:
        await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('open'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    tmp = callback_query.data.split("===")
    number, text = int(tmp[1]), tmp[2]
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if number in instance:
        await bot.send_message(callback_query.from_user.id, "Request is busy!")
    else:
        await bot.answer_callback_query(callback_query.id)
        instance[number] = {"id": callback_query.from_user.id, "status": "Open"}
        isBusy[callback_query.from_user.id] = number
        await bot.send_message(callback_query.from_user.id, "Here is the text of the question. Please answer with one "
                                                            "message!\n\n" + text)
        await bot.send_message(bot_id,
                               f"{number}==={database[callback_query.from_user.id]['Name']} connected to the chat!")


async def send_all_request(number, text):
    if number in instance:
        if text == "close":
            isBusy[instance[number]["id"]] = "0"
            await bot.send_message(instance[number]["id"], "Request closed!")
            instance.pop(number)
        else:
            await bot.send_message(instance[number]["id"], text)
    else:
        inline_btn_1 = InlineKeyboardButton('Start', callback_data=f'open==={number}==={text}')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
        for i in database:
            if database[i]["Type"] == "user" and isBusy[i] == "0":
                await bot.send_message(i, f"New request № {number}", reply_markup=inline_kb1)


@dp.message_handler()
async def new_request(message: types.Message):
    if database[message.chat.id]["Type"] == "admin":
        number = message.text.split('===')[0]
        text = message.text.split('===')[1]
        await send_all_request(int(number), text)
    elif isBusy[message.chat.id] != "0":
        if message.text == "close":
            await bot.send_message(bot_id, str(isBusy[message.chat.id]) + "===closed!")
            isBusy[instance[int(isBusy[message.chat.id])]["id"]] = "0"
            await bot.send_message(message.chat.id, "Thank you. Request closed!")
            instance.pop(int(isBusy[message.chat.id]))
        else:
            await bot.send_message(bot_id, str(isBusy[message.chat.id]) + "===" + message.text)
            databaseHandler.sheetWriteAnswer(int(isBusy[message.chat.id]), message.text)


def start_bot():
    read_data("volunteers.txt")
    executor.start_polling(dp, skip_updates=True)
