from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from app.handlers.audio_handler import handle_audio
from app.handlers.fallbacks import fallback
from app.handlers.start import start
from app.res.states import States
from app.settings.app import AppSettings


def main():
    settings = AppSettings()

    application = Application.builder().token(settings.token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.AUTH: [MessageHandler(filters.TEXT, start)],
            States.SEND_AUDIO: [MessageHandler(filters.AUDIO | filters.VOICE, handle_audio)]
        },
        fallbacks=[MessageHandler(filters.ALL, fallback)]
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
