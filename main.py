import transformers
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    Defaults,
)

from app.container import APP_CONTAINER
from app.handlers.audio_handler import handle_audio
from app.handlers.fallbacks import fallback
from app.handlers.start import start
from app.res.states import States

transformers.logging.set_verbosity_info()


def main():
    settings = APP_CONTAINER.app_settings()
    APP_CONTAINER.stt_adapter()
    defaults = Defaults(block=False)

    application = Application.builder().token(settings.token).defaults(defaults).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT, start),
        ],
        states={
            States.AUTH: [MessageHandler(filters.TEXT, start)],
            States.SEND_AUDIO: [
                MessageHandler(filters.AUDIO | filters.VOICE, handle_audio)
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            MessageHandler(filters.ALL, fallback),
        ],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
