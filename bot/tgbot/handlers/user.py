import fnmatch
import sqlite3
import os
import os.path
from PIL import Image
from aiogram import Dispatcher, Bot
from aiogram.types import Message, ContentType, InputFile
from aiogram.dispatcher import FSMContext
from pyffmpeg import FFmpeg
from db_py.db import Database
from tgbot.keyboards.inline import admin_keyboard
from tgbot.config import load_config

ff = FFmpeg()
db = Database()
config = load_config(".env.dist")


async def user_start(message: Message):
    try:
        db.add_user(message.chat.id, message.chat.username, message.chat.full_name, str(message.date))
    except sqlite3.IntegrityError:
        pass
    await message.answer("""⚙️ Уникализатор Медиа ⚙️
📌   Этот бот был создан специально для уникализации креативов для Facebook/Google/YouTube

🤔 Что умеет этот бот: 

✅ Меняет исходный код видео.
✅ Накладывает невидимые элементы на видео.
✅ Меняет звуковую дорожку. 
✅ Удаляет метаданные.
✅ 99% захода креативов.
                        """)
    await message.answer("⚠️ Отправьте боту видео (MP4) или фото (JPEG) до 20МБ или с меньшим разрешением!")


async def convert_media(message: Message):
    if message.text != "/admin":
        if message.content_type == "photo":
            await message.photo[-1].download()
            listOfFiles = os.listdir('./photos')
            pattern = "*.jpg"
            file = []
            for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                    file.append(entry)
            photo = Image.open(f"./photos/{file[0]}")
            photo = photo.rotate(0.01)
            photo.save(f"./photos/{file[0]}")
            photo = InputFile(f"./photos/{file[0]}")
            await message.answer_photo(photo)
            await message.answer_document(InputFile(f"./photos/{file[0]}"))
            os.remove(f"./photos/{file[0]}")
        elif message.content_type == "video":
            await message.video.download()
            await message.answer("💤 Обработка началась!")
            listOfFiles = os.listdir('./videos')
            pattern_1 = "*.MP4"
            pattern_2 = "*.mp4"
            pattern_3 = "*.MOV"
            file = []
            for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern_1):
                    file.append(entry)
            if not file:
                for entry in listOfFiles:
                    if fnmatch.fnmatch(entry, pattern_2):
                        file.append(entry)
            if not file:
                for entry in listOfFiles:
                    if fnmatch.fnmatch(entry, pattern_3):
                        file.append(entry)
            input_file = f"./videos/{file[0]}"
            ff.options(f"-i {input_file} -i transparent.png -filter_complex overlay=5:5 ./videos/video.mp4")
            await message.answer_video(InputFile('./videos/video.mp4'))
            os.remove(input_file)
            os.remove("./videos/video.mp4")
        if message.content_type == "document":
            if "photo" in message.document.mime_type:
                await message.document.download()
                listOfFiles = os.listdir('./documents')
                pattern = "*.jpg"
                file = []
                for entry in listOfFiles:
                    if fnmatch.fnmatch(entry, pattern):
                        file.append(entry)
                photo = Image.open(f"./documents/{file[0]}")
                photo = photo.rotate(0.01)
                photo.save(f"./documents/{file[0]}")
                photo = InputFile(f"./documents/{file[0]}")
                await message.answer_photo(photo)
                await message.answer_document(InputFile(f"./documents/{file[0]}"))
                os.remove(f"./documents/{file[0]}")
            elif "video" in message.document.mime_type:
                await message.document.download()
                await message.answer("💤 Обработка началась!")
                listOfFiles = os.listdir('./documents')
                pattern_1 = "*.MP4"
                pattern_2 = "*.mp4"
                pattern_3 = "*.MOV"
                file = []
                for entry in listOfFiles:
                    if fnmatch.fnmatch(entry, pattern_1):
                        file.append(entry)
                if not file:
                    for entry in listOfFiles:
                        if fnmatch.fnmatch(entry, pattern_2):
                            file.append(entry)
                if not file:
                    for entry in listOfFiles:
                        if fnmatch.fnmatch(entry, pattern_3):
                            file.append(entry)
                input_file = f"./documents/{file[0]}"
                ff.options(f"-i {input_file} -i transparent.png -filter_complex overlay=5:5 ./documents/video.mp4")
                await message.answer_document(document=InputFile('./documents/video.mp4'))
                os.remove(input_file)
                os.remove("./documents/video.mp4")
    else:
        if message.chat.id in config.tg_bot.admin_ids:
            await message.answer(text="Панель админа", reply_markup=admin_keyboard)


async def admin(message: Message):
    await message.answer(text="Панель админа", reply_markup=admin_keyboard)


async def mailing(message: Message, state: FSMContext):
    users = db.select_all_users()
    await message.answer("Рассылка начата")
    for user in users:
        bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
        await bot.send_message(chat_id=user[0], text=message.text)
        await bot.session.close()
    await message.answer("Рассылка завершена")
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(mailing, is_admin=True, state="Mailing:mailing_message", content_types=ContentType.ANY)
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(convert_media, state="*", content_types=ContentType.ANY)
    dp.register_message_handler(admin, state="*", is_admin=True)
