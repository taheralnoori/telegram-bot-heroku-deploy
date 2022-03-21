# -*- coding: utf-8 -*-
# MyBot https://t.me/Urlsepdfbot 
#[if url doesn't work on desktop use mobile to open]
# how to use
# =========================================
# add auth token first
# run the file
# go to telegram
# /start cmd : (optional) to see start msg
# /help cmd : (optional) to get help
# to convert url2pdf just type url (required)
# dont type /start again to download file

# ===========================================

import logging
import pdfkit

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
token ='5053664176:AAEzg5wkWsb9Lkbdsh0zDJqyynmetnfRl9E'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('URL2PDF')


# downloading pdf file
def download(url):
    logger.info("pdf downloading")
    # wkhtl2pdf options
    options={
        "load-error-handling": "ignore",
        "load-media-error-handling":"ignore",
        "stop-slow-scripts":"",
        "disable-local-file-access":"",
        "javascript-delay":10000, 
    }
    #handling errors
    try:
        pdfkit.from_url(url, 'out.pdf' ,options=options)
    except :
        #handle any type of error occured during downloading pdf file
        error = sys.exc_info()[0]
        #these errors are thrown by pdfkit while using wkhtml2pdf under the hood
        logger.warning(error," : an error occured: pdf file may miss some content")
    finally:
        #finally pass the as much downloaded file further
        pass;

# get url from user
def geturl(update, context):
    """Accept url"""
    logger.info('Url2pdf')
    chat_id = update.message.chat_id
    url = update.message.text
    logger.info("url => {}".format(url))
    download(url)
    logger.info("pdf downloaded")
    context.bot.send_document(chat_id=chat_id, document=open('out.pdf', 'rb'))
    logger.info('pdf sent')


# start cmd
def start(update,context):
    logger.info('starting cmd')
    # Shortcut for: bot.send_message(update.message.chat_id, *args, **kwargs)
    update.message.reply_text("👋 hey let\'s start...")


# help cmd
def help(update,context):
     logger.info("help cmd")
     update.message.reply_text("hey 👋\nhappy to help you...😊")



# error handler callback
def errorHandler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("error:file too long")


if __name__ == '__main__':
    print("welcome to url2pdf")
    #Updater: Its purpose is to receive the updates from Telegram and to deliver them to said dispatcher
    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    # dispatches all kinds of updates to its registered handlers.
    dp = updater.dispatcher

    # error handling
    # log all errors
    dp.add_error_handler(errorHandler)

    # handling commands
    # commands starts with / in telegram
    dp.add_handler(CommandHandler(['start'], start))    #/start
    dp.add_handler(CommandHandler(['help'], help))      #/help

     # on noncommand i.e message - echo the message on Telegram
    #allow handling of text msgs only
    dp.add_handler(MessageHandler(Filters.text, geturl))

    # Start the Bot
    # Starts polling updates from Telegram.
    updater.start_polling(timeout=60)
    updater.idle()
