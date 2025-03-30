import json

from flask import Flask, request, render_template
import os
import threading
import Textbelt
from config import config_instance

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

    if config_instance.get_config_value('enable sms'):
        phone_number = config_instance.get_config_value('phone number')
        message = f"SEIZURE ALERT: {config_instance.get_config_value('help message')}"
        Textbelt.send_text_message(phone_number, message)

    vars = {
        'contact': config_instance.get_config_value('contact'),
    }

    return render_template('help.html', **vars)


# @app.route('/config')
# def config():
#     print('config')
#
#     vars = {
#         'contact': get_config_value('contact'),
#     }
#
#     return render_template('config.html', **vars)


@app.route('/config', methods=['GET', 'POST'])
def config():
    message = None
    if request.method == 'POST':
        new_settings = request.form.to_dict()
        print("New settings submitted:", new_settings)
        message = "Config updated"
        config_instance.set_config(new_settings)

    # Render the form template with the settings and message (if any)
    print(f"config is {config_instance.get_config()}")
    return render_template('config.html', message=message, settings=config_instance.get_config())


@app.route('/alert/no') #TODO
def alert_no():
    pass
