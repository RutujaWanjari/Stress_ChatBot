from project import app
from flask import render_template, request
from project.controllers import nlp


message_list = []
@app.route('/', methods=['GET','POST'])
def index():
    try:
        message = request.form['message_input']
        bot_response = nlp.bot_response(message)
        m1 = [message, str(bot_response)]
        message_list.append(m1)
        return render_template('layout/index.html', message_list=message_list)
    except Exception as e:
        return render_template('layout/index.html')
