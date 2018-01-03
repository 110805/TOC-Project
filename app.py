import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '513813287:AAHeRZsswSWMqoK6DwEVS4aa9Cn6bcWAfnI'
WEBHOOK_URL = 'https://cdc9dd7a.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'init',
        'hello',
        'name',
        'reply_name',
        'recommend'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'hello',
            'conditions': 'say_hi'
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'name',
            'conditions': 'say_name'
        },
        {
            'trigger': 'advance',
            'source': 'name',
            'dest': 'reply_name',
            'conditions':'reply'
        },
        {
            'trigger':'advance',
            'source':'init',
            'dest':'recommend',
            'conditions':'choice'
        },
        {
            'trigger':'go_back',
            'source':['hello','name'],
            'dest':'init',
        }
    ],
    initial='init',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
