from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from db_py.db import Database
from tgbot.keyboards.inline import sub_admin_keyboard, negative_feedback_client_keyboard
from tgbot.config import load_config
from datetime import datetime
from tgbot.misc.states import Mailing
from aiogram import Dispatcher, Bot
import aioschedule
import asyncio

db = Database()
config = load_config(".env.dist")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def statistics(call: CallbackQuery):
    if call.message.chat.id in config.tg_bot.admin_ids:
        await call.message.edit_text(text="Кнопки статистики:", reply_markup=sub_admin_keyboard)


async def all_time(call: CallbackQuery):
    if call.message.chat.id in config.tg_bot.admin_ids:
        text = []
        users = db.select_all_users()
        for user in users:
            if user[1] is None:
                text.append(user[2])
            else:
                text.append(f"@{user[1]}")
        await call.message.edit_text(text="\n".join(text), reply_markup=sub_admin_keyboard)


async def last_7_days(call: CallbackQuery):
    if call.message.chat.id in config.tg_bot.admin_ids:
        text = []
        users = db.select_all_users()
        for user in users:
            date_time_str = user[3].replace("-", " ")
            date_time_obj = datetime.strptime(date_time_str, "%Y %m %d %H:%M:%S")
            if int((datetime.today() - date_time_obj).days) <= 7:
                if user[1] is None:
                    text.append(user[2])
                else:
                    text.append(f"@{user[1]}")
        await call.message.edit_text(text="\n".join(text), reply_markup=sub_admin_keyboard)
        await bot.send_message(config.tg_bot.admins_chat, "\n".join(text))


async def last_24_hours():
    text = []
    users = db.select_all_users()
    for user in users:
        date_time_str = user[3].replace("-", " ")
        date_time_obj = datetime.strptime(date_time_str, "%Y %m %d %H:%M:%S")
        if int((datetime.today() - date_time_obj).days) <= 1:
            if user[1] is None:
                text.append(user[2])
            else:
                text.append(f"@{user[1]}")
    await bot.send_message(config.tg_bot.admins_chat, "\n".join(text))


async def scheduler():
    aioschedule.every().day.at("00:01").do(last_24_hours)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def mailing(call: CallbackQuery):
    await Mailing.mailing_message.set()
    await call.message.answer("Введите сообщение для рассылки")


async def positive_feedback(call: CallbackQuery):
    await call.message.edit_text(text="Спасибо за использование нашего бота, удачных заливов! 🤑")


async def negative_feedback(call: CallbackQuery):
    await call.message.edit_text(text="Для вас есть спецпредложение 🔥", reply_markup=negative_feedback_client_keyboard)



def register_inline(dp: Dispatcher):
    dp.register_callback_query_handler(statistics, text="statistics", state="*")
    dp.register_callback_query_handler(all_time, text="all_time", state="*")
    dp.register_callback_query_handler(last_7_days, text="last_7_days", state="*")
    dp.register_callback_query_handler(mailing, text="mailing", state="*")
    dp.register_callback_query_handler(positive_feedback, text="positive_feedback", state="*")
    dp.register_callback_query_handler(negative_feedback, text="negative_feedback", state="*")

