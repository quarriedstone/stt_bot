import io
import textwrap
from typing import TYPE_CHECKING

from telegram.ext import ConversationHandler

import app.res.messages as messages
from app.container import APP_CONTAINER
from app.logger import logger
from app.res import keyboards
from telegram import ReplyKeyboardMarkup

from app.res.states import States


if TYPE_CHECKING:
    from telegram import File


async def handle_audio(update, context):
    stt_adapter = APP_CONTAINER.stt_adapter()
    app_settings = APP_CONTAINER.app_settings()

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

    logger.info(f"Starting to process: {file.file_path}")
    text = stt_adapter.stt_to_text(in_memory_file)
    text_chunks = textwrap.wrap(text, app_settings.chunk_size)

    logger.info(f"Ending to process: {file.file_path}")

    for i, message in enumerate(text_chunks):
        logger.debug(f"Chunk {i}: {message}")
        await update.message.reply_text(message)

    await update.message.reply_text(
        messages.RESTART,
        reply_markup=ReplyKeyboardMarkup(
            keyboards.START,
            one_time_keyboard=True,
        ),
    )

    return States.SEND_AUDIO
