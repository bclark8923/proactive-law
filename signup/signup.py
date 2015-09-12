from flask import Flask, request, redirect, session
import twilio.twiml
from parse_rest.user import User
from parse_rest.connection import register

register(<application_id>, <rest_api_key>[, master_key=None])
 
# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)
 
 
@app.route("/", methods=['POST'])
def hello_monkey():
    """Main method to handle incoming SMS."""
 
    from_number = request.values.get('From')
    user = User.Query.get(phone_number=from_number)
    if user and user.first_name and user.last_name and user.phone_number:
        resp = handle_inquery(user, request.values.get('Body'))
    else:
    	if not user:
    		user = User()
    		body = from_number
		else:
			body = request.values.get('Body')

        resp = signup_new_user(user, body)
 
    message = "".join([name, " has messaged ", request.values.get('To'), " ", 
        str(counter), " times."])
    resp = twilio.twiml.Response()
    resp.sms(message)
 
    return str(resp)


def signup_new_user(user, body=None):
	"""Registers new user."""
	resp = twilio.twiml.Response()
	if not user.phone_number:
		user.phone_number = body
		user.save()
		message = "Welcome to Proactive Law! Tell us your first name to get started."
	if not user.first_name:
		user.first_name = body
		user.save()
		message = "Hello %s, what's your last name?" % user.first_name
	else if not user.last_name:
		user.last_name = body
		user.save()
		message = "Welcome %s %s, we just need your birthdate (MM/DD/YYYY) to verify your identity" % (user.first_name, user.last_name)
	else if not user.birthdate:
		user.birthdate = "%s 0:00" % body
		message =  "%s, Thanks for signing up for Proactive Law! How can we help you? (You can type HElP for a list of options)" % user.first_name
	else:
		"Welcome %s %s, how can we help you today? (You can type HElP for a list of options)" % (user.first_name, user.last_name)
    resp.sms(message)
	return resp 

def handle_inquery(user, body=None):
	"""Handles incoming requests."""
	resp = twilio.twiml.Response()
	if body == "HELP":
		message = "Proactive Law is here to help you with your legal questions, 24/7.\n"
				  "Type CITATIONS to view outstanding citations.\n"
				  "WARRANT to view outstanding warrants.\n"
				  "SUBSCRIBE to send reminders on court proceedings.\n"
				  "PAY to pay outstanding bills.\n"


	resp.sms(message)
	return resp

if __name__ == "__main__":
    app.run(debug=True)