from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

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
    msg = msg.lower()
    print(msg)
    reply_file = reply_dir + msg + '.txt'
    try:
        f = open(reply_file, 'r')
    except:
        f = open('./reply/exception.txt', 'r')
    reply_msg = f.read()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
if __name__ == "__main__":
    app.run()
