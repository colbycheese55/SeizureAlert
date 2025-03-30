from flask import Flask, render_template
import os
import threading
import Textbelt
from config import get_config_value

templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
app = Flask(__name__, template_folder=templates_path)

seizure = threading.Event()
alert_text = None


@app.route('/alert')
def home():
    vars = {
        'text': alert_text,
        'counter': 10,
    }

    return render_template('alert.html', **vars)


@app.route('/help')
def help_needed():
    print('help_needed')

    if get_config_value('enable_sms'):
        phone_number = get_config_value('phone number')
        message = f"SEIZURE ALERT: {get_config_value('help_message')}"
        Textbelt.send_text_message(phone_number, message)

    vars = {
        'contact': get_config_value('contact'),
    }

    return render_template('help.html', **vars)


@app.route('/alert/no') #TODO
def alert_no():
    pass
