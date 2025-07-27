import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hbold

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
file = open("SAVE_FOLDER.txt")
SAVE_FOLDER = file.read()
file.close()

os.makedirs(SAVE_FOLDER, exist_ok=True)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        f"Привет, {hbold(message.from_user.first_name)}! Отправь мне любой файл, и я сохраню его."
    )

@dp.message(F.document)
async def handle_document(message: types.Message):
    """Обработчик документов"""
    document = message.document
    file_name = document.file_name or f"file_{document.file_id}"
    save_path = os.path.join(SAVE_FOLDER, file_name)
    
    await bot.download(
        document,
        destination=save_path
    )
    
    await message.answer(
        f"Документ {hbold(file_name)} успешно сохранен!"
    )

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    """Обработчик фото"""
    photo = message.photo[-1]  # Берем фото с самым высоким разрешением
    file_name = f"photo_{photo.file_id}.jpg"
    save_path = os.path.join(SAVE_FOLDER, file_name)
    
    await bot.download(
        photo,
        destination=save_path
    )
    
    await message.answer(
        f"Фото сохранено как {hbold(file_name)}!"
    )

@dp.message(F.audio)
async def handle_audio(message: types.Message):
    """Обработчик аудио"""
    audio = message.audio
    file_name = audio.file_name or f"audio_{audio.file_id}.mp3"
    save_path = os.path.join(SAVE_FOLDER, file_name)
    
    await bot.download(
        audio,
        destination=save_path
    )
    
    await message.answer(
        f"Аудиофайл {hbold(file_name)} сохранен!"
    )

@dp.message(F.video)
async def handle_video(message: types.Message):
    """Обработчик видео"""
    video = message.video
    file_name = video.file_name or f"video_{video.file_id}.mp4"
    save_path = os.path.join(SAVE_FOLDER, file_name)
    
    await bot.download(
        video,
        destination=save_path
    )
    
    await message.answer(
        f"Видеофайл {hbold(file_name)} сохранен!"
    )

@dp.message(F.voice)
async def handle_voice(message: types.Message):
    """Обработчик голосовых сообщений"""
    voice = message.voice
    file_name = f"voice_{voice.file_id}.ogg"
    save_path = os.path.join(SAVE_FOLDER, file_name)
    
    await bot.download(
        voice,
        destination=save_path
    )
    
    await message.answer(
        f"Голосовое сообщение сохранено как {hbold(file_name)}!"
    )

async def main():
    """Запуск бота"""
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())