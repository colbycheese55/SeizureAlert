from flask import Flask, render_template, send_from_directory
import os

templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
app = Flask(__name__, template_folder=templates_path)
print(app.template_folder)


@app.route('/alert')
def home():
    vars = {
        'text': 'Hello World!',
        'timer': 10,
    }

    return render_template('alert.html', **vars)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)