import os
import time
import logging
from telegram import ChatAction
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

import qrcode
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
INPU = range(4)


def start(update, context):

    update.message.reply_text("Qué deseas hacer?\n\n Usa \Qr para generar un qr")

def qr_command_handler(update, context):
    update.message.reply_text("Envía el texto para generar el qr:\n")
    return INPU

def generate_qr(text):

    filename = text + ".jpg"
    image = qrcode.make(text)
    image.save(filename)
    return filename


def send_qr(img, chat):

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout = None
    )
    
    
    chat.send_photo(
        photo = open(img, 'rb')
    )
    
    os.unLink(img)

def inputtext(update,context):
    #bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    text = update.message.text #here because we want to retrieve the text from the original message and send the same thing back
    chat = update.message.chat
    
    filename = generate_qr(text)
    send_qr(filename, chat)
    return ConversationHandler.END

def main() -> None:

    updater = Updater("5202799890:AAESmZj4AR7SsTo6UlJUQYnR5Mbnq-bBWEM")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('qr', qr_command_handler)],
        states={
            INPU: [MessageHandler(Filters.text & ~Filters.command, inputtext)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()


    updater.idle()
if __name__ == '__main__':
    main()