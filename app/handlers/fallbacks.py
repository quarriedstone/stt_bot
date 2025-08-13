from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from app.logger import logger
from app.res import messages, keyboards


async def fallback(update, context):
    logger.info("fallback")
    await update.message.reply_text(
        messages.FALLBACK,
        reply_markup=ReplyKeyboardMarkup(
            keyboards.START,
            one_time_keyboard=True,
        ),
    )

    return ConversationHandler.END
