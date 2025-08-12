import io
from typing import TYPE_CHECKING

from telegram.ext import ConversationHandler

import app.res.messages as messages
from app.logger import logger

from app.res.states import States

if TYPE_CHECKING:
    from telegram import File


async def handle_audio(update, context):
    logger.info("handle_audio")

    if update.message.audio:
        file_id = update.message.audio.file_id
    elif update.message.voice:
        file_id = update.message.voice.file_id
    else:
        await update.message.reply_text(messages.FALLBACK)
        return ConversationHandler.END

    file: "File" = await context.bot.get_file(file_id)

    await update.message.reply_text(messages.AUDIO_STARTED)

    in_memory_file = io.BytesIO()
    await file.download_to_memory(in_memory_file)
    in_memory_file.seek(0)

    await update.message.reply_text(F"Файл {file.file_id}, размер {len(in_memory_file.getvalue())}")

    return States.AUTH
