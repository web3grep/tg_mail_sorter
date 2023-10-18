from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat
import logging
from settings import TOKEN, SCAN_CHANNEL_ID, NOTIFICATION_CHAT_ID

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

keywords = set()

def start(update, context):
    update.message.reply_text("Бот запущен. Добавьте ключевые слова с помощью команды /add_keyword.")

def add_keyword(update, context):
    keyword = update.message.text.split()[-1]
    keywords.add(keyword)
    update.message.reply_text(f"Ключевое слово '{keyword}' добавлено.")

def handle_message(update, context):
    if update.channel_post:
        message = update.channel_post
        for keyword in keywords:
            if keyword in message.text:
                context.bot.send_message(chat_id=NOTIFICATION_CHAT_ID, text=f"New mail: {keyword}\n {message.link}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add_keyword", add_keyword))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
