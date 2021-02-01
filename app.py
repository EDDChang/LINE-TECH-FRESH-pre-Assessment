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
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='test'))
    return
    try:
        f = open(reply_file, 'r')
    except:
        f = open('./reply/exception.txt', 'r')
        reply_msg = r.read()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
        return
    
    reply_msg = f.read()
    
    if msg != 'info':
        reply_msg = f.read().split('\n')
        for sentence in reply_msg:
            time.sleep(2.5)
            line_bot_api.push_message(event.source.sender_id, TextSendMessage(text=sentence))
    else:
        reply_msg = f.read()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
    
    f.close()
if __name__ == "__main__":
    app.run()
