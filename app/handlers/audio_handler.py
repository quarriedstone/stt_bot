import io
import textwrap
from typing import TYPE_CHECKING

from telegram.ext import ConversationHandler

import app.res.messages as messages
from app.container import APP_CONTAINER
from app.logger import logger
from app.res.mime_types import MimeTypes
from app.res.states import States

if TYPE_CHECKING:
    from telegram import File


async def handle_audio(update, context):
    stt_adapter = APP_CONTAINER.stt_adapter()
    app_settings = APP_CONTAINER.app_settings()
    audio_adapter = APP_CONTAINER.audio_adapter()

    supported_mime_types = [MimeTypes.mp3, MimeTypes.wav, MimeTypes.ogg]

    logger.info("handle_audio")

    if update.message.audio:
        file_id = update.message.audio.file_id
        mime_type = update.message.audio.mime_type
    elif update.message.voice:
        file_id = update.message.voice.file_id
        mime_type = update.message.voice.mime_type
    else:
        await update.message.reply_text(messages.FALLBACK)
        return ConversationHandler.END

    file: "File" = await context.bot.get_file(file_id)

    await update.message.reply_text(messages.AUDIO_STARTED)

    in_memory_file = io.BytesIO()
    await file.download_to_memory(in_memory_file)
    in_memory_file.seek(0)

    if mime_type == MimeTypes.m4a:
        in_memory_file = audio_adapter.convert_m4a_to_mp3_in_memory(in_memory_file)
    elif mime_type not in supported_mime_types:
        logger.debug(f"Unsupported file type: {mime_type}")
        await update.message.reply_text(
            messages.UNSUPPORTED_FILE.format([*supported_mime_types, MimeTypes.m4a])
        )
        return ConversationHandler.END

    logger.info(f"Starting to process: {file.file_path}")
    text = stt_adapter.stt_to_text(in_memory_file)
    text_chunks = textwrap.wrap(text, app_settings.chunk_size)

    logger.info(f"Ending to process: {file.file_path}")

    for i, message in enumerate(text_chunks):
        logger.debug(f"Chunk {i}: {message}")
        await update.message.reply_text(message)

    await update.message.reply_text(
        messages.RESTART,
    )

    return States.SEND_AUDIO
