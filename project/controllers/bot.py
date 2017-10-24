# from flask import render_template
# from flask_wtf import Form
# from wtforms import StringField
# from wtforms.validators import DataRequired
# from flask import request
# from flask_login import LoginManager, login_required, logout_user
# # for API
# # Note - urllib.request changes POST methods to GET, hence used requests library for cancel transaction
# import urllib.request, urllib.parse, urllib.error
# import json
# import requests
# # for communication inside project
# from project import app
# from project.controllers.loginAuthentication import User
# from project.controllers.genrateIntent import NLP
# #for mail
# from flask_mail import Message
# from project import mail
# from project import ADMINS
# #for db
# from project.db.mongo import *
# from project import socketio
# #logout user
# from flask import session
# import apiai
#
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login_def"
# message_list = []
# message = ""
# nlp_obj = NLP()
#
#
# # Main  route
# @app.route('/', methods=['GET','POST'])
# def start_def():
#     # session['user_name'] = 'hero'
#     try:
#         user = logout_user()
#         # session.pop(user)
#         # disconnect_user()
#     except Exception as e:
#         print(str(e))
#     form = CreateForm(request.form)
#     return render_template('printer/index.html', form=form)
#
#
# # Used for logging/debugging in jinja code
# @app.context_processor
# def utility_functions():
#     def print_in_console(message):
#         print(message)
#     return dict(mdebug=print_in_console)
#
#
# # Utility function to split date and time in transaction status template
# def splitpart (value, index, char = ' '):
#     return value.split(char)[index]
#
#
# # Default form element
# class CreateForm(Form):
#     text = StringField('name', validators=[DataRequired()])
#
#
# global context
# def api_def(user_text):
#     try:
#         # Set API.ai client
#         ai = apiai.ApiAI("cc96141fd1bc443ca4ebd86be11555a1")
#         request = ai.text_request()
#         request.query = user_text
#         request.lang = 'en'
#         global context
#         try:
#             if context != None:
#                 request.contexts = context
#         except:
#             context = None
#         # Receiving the response.
#         response = json.loads(request.getresponse().read().decode('utf-8'))
#         responseStatus = response['status']['code']
#         try:
#             if response['result']['action'] == 'input.unknown':
#                 last_msg = message_list[-1]
#                 last_msg = last_msg[0]
#                 user_text = last_msg + " " + user_text
#                 return api_def(user_text)
#             if response['result']['contexts']:
#                 context = response['result']['contexts']
#             else:
#                 context = None
#         except Exception as e:
#             context = None
#             if response['result']['action'] == 'input.unknown':
#                 last_msg = message_list[-1]
#                 last_msg = last_msg[0]
#                 user_text = last_msg + " " + user_text
#                 return api_def(user_text)
#         # Return template or text response
#         if (responseStatus == 200):
#             try:
#                 if response['result']['fulfillment']['messages'][1]['payload']['template']:
#                     template = response['result']['fulfillment']['messages'][1]['payload']['template']
#                     return template
#             except:
#                 return (response['result']['fulfillment']['speech'])
#         else:
#             return ("Sorry, can you rephrase your query")
#             # NOTE:
#             # At the moment, all messages sent to ApiAI cannot be differentiated,
#             # they are processed as a single conversation regardless of concurrent
#             # conversations. We need to perhaps peg a session id (ApiAI) to a recipient
#             # id (Messenger) to fix this.
#             # request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
#     except Exception as e:
#         return "Could not get response."
#
#
# # Used for all purposes
# @app.route('/respond', methods=['POST'])
# def respond_def():
#     try:
#         message = request.form['message_input']
#     except:
#         message = "Hello"
#     answer = api_def(message)
#     return answer
#
#
# # Login route
# @app.route('/login', methods=['GET','POST'])
# def login_def():
#     if request.method == 'POST':
#         email =  request.form['lg_username']
#         password = request.form['lg_password']
#         responseData = None
#         try:
#             details = urllib.parse.urlencode({'EmailId': email, 'Password': password})
#             details = details.encode('UTF-8')
#             url = urllib.request.Request('http://stagingapi.instarem.com/v1/api/v1/Login', details)
#             url.add_header("Authorization", "amx 0O1QCg+UcMLTHdfxHJllzWiUfWTw520EMifGt72vTDmRgMXZKJsx001K2Svelvuh")
#             url.add_header("Content-Type", "application/x-www-form-urlencoded")
#             responseData = urllib.request.urlopen(url).read().decode('utf8','ignore')
#             responseFail = False
#         except urllib.error.HTTPError as e:
#             responseData = e.read().decode('utf8', 'ignore')
#             responseFail = False
#         except Exception as e:
#             responseFail = True
#         responseData = json.loads(responseData)
#         print(responseData)
#         session['api_session_token'] = responseData["authToken"]
#         if responseData["statusCode"] == 200:
#             return json.dumps({'statusCode': responseData["statusCode"], 'statusMessage': responseData['statusMessage']})
#         else:
#             return json.dumps({'statusCode': responseData["statusCode"], 'statusMessage': responseData['statusMessage']})
#
#
# @socketio.on('disconnect')
# def disconnect_user():
#     logout_user()
#     session.pop(app.config['SECRET_KEY'], None)
#
# # Logout route
# @app.route("/logout")
# @login_required
# def logout_def():
#     logout_user()
#     return json.dumps({'statusCode': 200, 'statusMessage': 'Logged out successfully'})
#
#
# # Callback to reload the user object
# @login_manager.user_loader
# def load_user(id):
#     return User(id, "auuser@instarem.com", "Abc@123")
#
#
# # Fx check route
# @app.route('/fx', methods=['GET', 'POST'])
# def fx_check_def():
#     if request.method == 'POST':
#         from_curr = request.form.get('from_curr')
#         to_curr = request.form.get('to_curr')
#         url_send  = "http://api.instarem.com/api/v1/FxRate?from="+ from_curr + "&to=" + to_curr + "&timeOffset=330"
#         auth_token = "amx 0O1QCg+UcMLTHdfxHJllzWiUfWTw520EMifGt72vTDmRgMXZKJsx001K2Svelvuh"
#         responseData = instarem_api(url_send, auth_token, None)
#         responseData = json.loads(responseData)
#         messages = ["fxRate", responseData["responseData"][0]]
#         message_list.append(messages)
#         responseData = [from_curr, to_curr, responseData["responseData"][0]]
#         return json.dumps({'statusCode': 200, 'response':responseData})
#     return json.dumps({'statusCode': 401, 'response': 'fail'})
#
#
# # Call Instarem APIs and retutn resonse
# def instarem_api(root_url, auth_token, body_code = None):
#     try:
#         url = urllib.request.Request(root_url)
#         if auth_token:
#             url.add_header("Authorization", auth_token)
#         url.add_header("Content-Type", "application/x-www-form-urlencoded")
#         responseData = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
#         return responseData
#     except Exception as e:
#         return
#
#
# # Transaction status route
# @login_required
# @app.route('/status', methods=['GET', 'POST'])
# def status_def():
#     trans_ids = request.form.getlist('refid')
#     trans_ID = ''.join(trans_ids)
#     url_send = "http://stagingapi.instarem.com/v1/api/v1/GetPaymentDetails?RefNumber=" + trans_ID
#     if session['api_session_token'] == None:
#         return json.dumps({'statusCode': 401, 'statusMessage': 'Please login'})
#     auth_token = 'amx ' +  session['api_session_token']
#     responseData = instarem_api(url_send, auth_token, None)
#     responseData = json.loads(responseData)
#     if responseData["statusCode"] == 200:
#         return json.dumps({'statusCode': responseData["statusCode"], 'response': responseData['responseData']})
#     else:
#         return json.dumps({'statusCode': responseData["statusCode"], 'statusMessage': responseData['statusMessage']})
#
#
# # Route for searching beneficiary in the beneficiary list
# @login_required
# @app.route('/beneficiarySearch', methods=['POST'])
# def bene_search_def():
#     auth_token = 'amx ' + session['api_session_token']
#     url_send = "http://stagingapi.instarem.com/v1/api/v1/GetPayeeList"
#     responseData = instarem_api(url_send, auth_token, None)
#     response = json.loads(responseData)
#     responseData = response["responseData"]
#     list = []
#     name = request.data.decode('utf8').split('=')[1]
#     for res in responseData:
#         if res["firstName"] == name:
#             dict = res
#             list.append(dict)
#     if response["statusCode"] == 200:
#         return json.dumps({'statusCode': 200, 'response':list})
#     else:
#         return json.dumps({'statusCode': 503, 'statusMessage': "Could not get beneficiary list"})
#
#
# # this shows the beneficiary details of the person and list them all from a JSON format
# @login_required
# @app.route('/beneficiary', methods=['GET', 'POST'])
# def beneficiary_def():
#     if session['api_session_token'] == None:
#         return json.dumps({'statusCode': 401, 'statusMessage': 'Please login'})
#     auth_token = 'amx ' +  session['api_session_token']
#     url_send = "http://stagingapi.instarem.com/v1/api/v1/GetPayeeList"
#     responseData = instarem_api(url_send , auth_token, None)
#     responseData = json.loads(responseData)
#     if responseData["statusCode"] == 200:
#         return json.dumps({'statusCode': 200, 'response': responseData["responseData"]})
#     else:
#         return json.dumps({'statusCode': 503, 'statusMessage': "Could not get beneficiary list"})
#
#
# # Send mail to instarem support
# @app.route('/sendmail', methods=['GET', 'POST'])
# def send_mail_def():
#     msg = Message('From bot', sender=ADMINS[0], recipients=ADMINS)
#     msg.body = request.form.get("message")
#     with app.app_context():
#         try:
#             mail.send(msg)
#             flag = True
#         except:
#             flag = False
#     if flag:
#         return json.dumps({'statusCode': 200, 'statusMessage': 'Thankyou for your feedback.'})
#     else:
#         return json.dumps({'statusCode': 404, 'statusMessage': 'Sorry, we could not get your feedback.'})
#
#
# # Cancel transaction of a particular user
# @login_required
# @app.route('/cancel', methods=['GET', 'POST'])
# def cancel_def():
#     if request.method == 'POST':
#        try:
#            transact_ID = request.form.get('t_id')
#            url = 'http://stagingapi.instarem.com/v1/api/v1/TransferCancelByUser?RefNumber=' + transact_ID
#            auth_token = 'amx ' + session['api_session_token']
#            headers = {'Content-Type': 'application/x-www-form-urlencoded',
#                       'Authorization': auth_token}
#            req = requests.post(url, headers=headers)
#            responseData = req.json()
#            if responseData["statusCode"] == 200:
#                return json.dumps({'statusCode': 200, 'statusMessage': responseData["statusMessage"]})
#            else:
#                return json.dumps({'statusCode': 503, 'statusMessage': "Could not cancel transaction"})
#        except Exception as e:
#            return json.dumps({'statusCode': 503, 'statusMessage': "Could not cancel transaction"})



from project import app
from flask import render_template

@app.route('/')
def index():
    return render_template('layout/index.html')