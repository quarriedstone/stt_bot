from app.logger import logger
from app.res.states import States
from app.settings.app import AppSettings
import app.res.messages as messages

service_settings = AppSettings()


async def start(update, context):
    logger.info("start")
    user_id = update.message.from_user.id
    if user_id in service_settings.users:
        await update.message.reply_text(messages.START_SUCCESS)
    else:
        await update.message.reply_text(messages.START_FAILED)

    return States.SEND_AUDIO
