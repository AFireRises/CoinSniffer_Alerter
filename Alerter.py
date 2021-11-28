#!/usr/bin/env python

"""
Alert for trending "good" poocoins
"""

import logging
import os
import requests

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# TODO find out how to make this local
schannel = ''
with open('.secret_channel','r') as fd:
    schannel = fd.read()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def id_trend_poocoins():
    url = "https://tokensniffer.com/"
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'}) # adjust user agent 

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    top_scoring_table = soup.find("div", attrs={"class": "Home_card__2SdtB"}) 
    top_scoring_data = top_scoring_table.find("table") # grab tr 

    coins = []
    for idx, td in enumerate(top_scoring_data.find_all("td")):
        if idx%2 == 0: # the table has timestamps in the other column
            coins.append(td.text)
    coins_msg = ' '.join([str(elem) for elem in coins])
    return coins_msg

def callback_minute(context: CallbackContext):

    message = id_trend_poocoins()
    context.bot.send_message(chat_id=schannel, 
                             text=message)

def main() -> None:
    stoken = 'Empty' # empty token

    with open('.secret_token', 'r') as fd:
        stoken = fd.read()
    
    # Create the Updater and pass it your bot's token.
    updater = Updater(stoken)
    j = updater.job_queue

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Start timer based messaging
    job_minute = j.run_repeating(callback_minute, interval=24*60*60, first=10)

    # Start polling
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT
    updater.idle()

if __name__ == '__main__':
    main()
