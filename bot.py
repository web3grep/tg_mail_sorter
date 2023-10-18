from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

KEYWORDS = set()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Бот запущен. Добавьте ключевые слова с помощью команды /add_keyword.")
    logger.info(f"Command /start received from {update.message.from_user.username}")

def add_keyword(update: Update, context: CallbackContext) -> None:
    keyword = update.message.text.split(' ', 1)[1]
    KEYWORDS.add(keyword)
    update.message.reply_text(f"Ключевое слово '{keyword}' добавлено.")
    logger.info(f"Keyword '{keyword}' added by {update.message.from_user.username}")

def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    for keyword in KEYWORDS:
        if keyword in message_text:
            context.bot.send_message(chat_id=settings.NOTIFICATION_CHAT_ID, text=f"New mail from {keyword}\n[GO](https://t.me/c/{str(update.message.chat.id)[4:]}/{update.message.message_id})", parse_mode=ParseMode.MARKDOWN)
            logger.info(f"Keyword '{keyword}' found in message: {message_text}")

def error_callback(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update {update} caused error {context.error}")

def main():
    bot = Bot(token=settings.TOKEN)
    updater = Updater(token=settings.TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add_keyword", add_keyword))
    dp.add_handler(MessageHandler(Filters.text & Filters.group, handle_message))
    dp.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
