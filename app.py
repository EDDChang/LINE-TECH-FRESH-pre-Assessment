from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser
import time
reply_dir = './reply/'

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    msg = event.message.text
    msg = msg.strip().lstrip().rstrip()
    msg = msg.lower()
    reply_file = reply_dir + msg + '.txt'
    exception = False
    try:
        f = open(reply_file, 'r')
    except:
        f = open('./reply/exception.txt', 'r')
        exception = True
    
    reply_msg = f.read()
    print(reply_msg)
    if msg == 'info' or exception:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
    else:
        reply_msg = reply_msg.split('\n')
        for sentence in reply_msg:
            line_bot_api.push_message(event.source.sender_id, TextSendMessage(text=sentence)) 
            time.sleep(2.5)
    f.close()
if __name__ == "__main__":
    app.run()
