from flask import Flask, request, redirect, session
import lob
import twilio.twiml
from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.query import QueryResourceDoesNotExist
import time
import re
from flask.ext.cors import CORS


app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

userClassName = "user"
User = Object.factory(userClassName)

citationClassName = "citations"
Citation = Object.factory(citationClassName)

violationClassName = "violations"
Violation = Object.factory(violationClassName)

lob.api_key = 'test_00f79ccdc57159f0a24923537e716623ebb'

@app.route("/payment", methods=['POST'])
def handle_payment():
	#TODO
	pass
 
@app.route("/", methods=['POST'])
def hello():
	"""Main method to handle incoming SMS."""
 
	from_number = request.values.get('From')
	body = request.values.get('Body')
	print request.values
	print from_number
	print body

	try:
		user = User.Query.get(phone_number=from_number)
	except QueryResourceDoesNotExist:
		user = User(first_name=None, last_name=None, phone_number=None, birthdate=None)
		body = from_number

	if user and user.first_name and user.last_name and user.phone_number and user.birthdate:
		resp = handle_inquery(user, body)
	else:
		resp = signup_new_user(user, body)
 
	return str(resp)


def signup_new_user(user, body=None):
	"""Registers new user."""
	resp = twilio.twiml.Response()
	if not user.phone_number:
		user.phone_number = body
		user.save()
		message = "Welcome to Proactive Law! Tell us your first name to get started and to subscribe to court proceedings."
	elif not user.first_name:
		user.first_name = body
		user.save()
		message = "Hello %s, what's your last name?" % user.first_name
	elif not user.last_name:
		user.last_name = body
		user.save()
		message = "Welcome %s %s, we just need your birthdate (MM/DD/YYYY) to verify your identity" % (user.first_name, user.last_name)
	elif not user.birthdate:
		user.birthdate = body
		user.save()
		message =  "%s, Thanks for signing up for Proactive Law! How can we help you? (You can type START for a list of options)" % user.first_name
	else:
		"Welcome %s %s, how can we help you today? (You can type START for a list of options)" % (user.first_name, user.last_name)
	resp.sms(message)
	print message
	return resp 

def handle_inquery(user, body=None):
	"""Handles incoming requests."""
	resp = twilio.twiml.Response()
	if body == "START":
		message = """Proactive Law is here to help you with your legal questions, 24/7.\n
				  Type CITATIONS to view outstanding citations.\n
				  VIOLATIONS to view outstanding violations.\n
				  WARRANTS to view outstanding warrants.\n
				  PAY to pay outstanding bills."""
	elif body == "CITATIONS":
		try:
			citations = Citation.Query.filter(
				first_name=user.first_name, last_name=user.last_name,
				date_of_birth=user.birthdate).order_by("citation_number")
		except QueryResourceDoesNotExist:
			message = "Congratulations! You currently have no oustanding citations"
			resp.sms(message)
			return resp

		citation_ids = []
		for citation in citations:
			citation_ids.append(citation.citation_number)

		"""
		try:
			violations = Violation.Query.filter(
				citation_number__in=citation_ids, status__nin=["CLOSED", "DISMISS WITHOUT COSTS"])
		except QueryResourceDoesNotExist:
			message = "Congratulations! You currently have no outstanding citations"
			resp.sms(message)
			return resp

		outstanding_citations = []
		for violation in violations:
			if violation.citation_number not in outstanding_citations:
				outstanding_citations.append(violation.citation_number)
		"""

		message = "You have %s outstanding citations:\n" % len(citations)
		index = 1
		for citation in citations:
			#if citation.citation_number in outstanding_citations:
			message = message + "%s) Citation number: %s with court proceeding date: %s at: %s, %s\n" % (
				index, int(citation.citation_number), citation.court_date.split(" ")[0], citation.court_address, citation.court_location.title())
			index = index + 1

		message = message + "Reply with the citation number to view a specific citation or enter START to view the main menu\n"
	# Match a citation
	elif re.match('^^[0-9]{8,9}$', body):
		pass
		#TODO
	elif body == "VIOLATIONS":
		try:
			citations = Citation.Query.filter(
				first_name=user.first_name, last_name=user.last_name,
				date_of_birth=user.birthdate).order_by("citation_number")
		except QueryResourceDoesNotExist:
			message = "Congratulations! You currently have no outstanding violations"
			resp.sms(message)
			return resp

		citation_ids = []
		for citation in citations:
			citation_ids.append(citation.citation_number)

		try:
			violations = Violation.Query.filter(
				citation_number__in=citation_ids, status__nin=["CLOSED", "DISMISS WITHOUT COSTS"]).order_by("violation_number")
		except QueryResourceDoesNotExist:
			message = "Congratulations! You currently have no outstanding violations"
			resp.sms(message)
			return resp

		message = "You have %s outstanding violations:\n" % len(violations)
		total_amount = 0
		for i, violation in enumerate(violations):
			message = message + "%s) Violation number: %s for: %s with fines: $%s" % (
				i+1, violation.violation_number, violation.violation_description, violation.court_cost + violation.fine_amount)
			if violation.warrant_status:
				message = message + " and warrant: %s issued\n" % violation.warrant_number
			else:
				message = message + "\n"
			total_amount = total_amount + violation.court_cost + violation.fine_amount

		message = message + "Your total amount owning is: $%s\n" % total_amount

		message = message + "Reply PAY violation number to pay a specific violation or enter START to view the main menu\n"

	elif body == "WARRANTS":
		try:
			citations = Citation.Query.filter(
				first_name=user.first_name, last_name=user.last_name,
				date_of_birth=user.birthdate).order_by("-citation_number")
		except QueryResourceDoesNotExist:
			message = "Congratulations! You currently have no outstanding warrants"
			resp.sms(message)
			return resp

		citation_ids = []
		for citation in citations:
			citation_ids.append(citation.citation_number)

		try:
			violations = Violation.Query.filter(
				citation_number__in=citation_ids, status__nin=["CLOSED", "DISMISS WITHOUT COSTS"], warrant_status=True)
		except QueryResourceDoesNotExist:
			message = "Congratulations! You currently have no outstanding warrants"
			resp.sms(message)
			return resp

		message = "You have %s outstanding warrants:\n" % len(violations)
		for i, violation in enumerate(violations):
			message = message + "%s) Warrant number: %s for: %s with violation number: %s and fines: $%s\n" % (
				i+1, violation.warrant_number, violation.violation_description, violation.violation_number, violation.court_cost + violation.fine_amount)

		message = message + "Reply PAY violation number to pay a specific violation or enter START to view the main menu\n"

	elif body.startswith("PAY"):
		if body == "PAY":
			message = """Please reply PAY violation number to pay a specific violation.\n
					  To view your outstanding violations, reply VIOLATIONS."""
			resp.sms(message)
			return resp
		
		violation_id = body.strip().split(" ")[1]
		try:
			violation = Violation.Query.get(violation_number=violation_id)
		except QueryResourceDoesNotExist:
			message = "Sorry, the violation number you entered was not found. Please try again or reply START to view the main menu."
			resp.sms(message)
			return resp

	# 	message = "You are about to pay $%s for Violation number: %s for: %s\n" % (violation.court_cost + violation.fine_amount, violation.violation_number, violation.violation_description)
	# 	message = message + """Which payment method would you liked to use?\n
	# 				SMS %s to pay by phone.\n
	# 				Reply CHECK and attach a picture of your check via MMS to pay by cheque\n
	# 				MONEYORDER and attach a picture of your money order via MMS to pay by money order.\n""" % violation.violation_number
	# elif body.startswith("SMS"):
	# 	if body == "SMS":
	# 		message = """Please reply SMS violation number to pay a specific violation.\n
	# 				  To view your outstanding violations, reply VIOLATIONS."""
	# 		resp.sms(message)
	# 		return resp

	# 	violation_id = body.strip().split(" ")[1]
		# try:
		# 	violation = Violation.Query.get(violation_number=violation_id)
		# except QueryResourceDoesNotExist:
		# 	message = "Sorry, the violation number you entered was not found. Please try again or reply START to view the main menu."
		# 	resp.sms(message)
		# 	return resp

		try:
			citation = Citation.Query.get(citation_number=violation.citation_number)
		except QueryResourceDoesNotExist:
			message = "Sorry, the violation number you entered was not found. Please try again or reply START to view the main menu."
			resp.sms(message)
			return resp

		cheque = lob.Check.create(
			  description = violation.violation_number,
			  to_address = {
				'name': citation.court_location + ' MUNICIPALITY COURT',
				'address_line1': citation.court_address,
				'address_city': citation.court_location.title(),
				'address_state': 'MO',
				'address_zip': '63301',
				'address_country': 'US'
			  },
			  bank_account = 'bank_ad79e048fe93310',
			  amount = violation.court_cost + violation.fine_amount,
			  memo = ("%s %s %s" % (user.first_name, user.last_name, violation.violation_number))[0:39],
			  logo = 'https://s3-us-west-2.amazonaws.com/lob-assets/lob_check_logo.png',
			  file = '<h2 style=\'padding-top:4in;\'>Check mailed on your behalf to {{court}} for violation {{violation}}</h2>',
			  data = {
				'court': citation.court_location + ' MUNICIPALITY COURT',
				'violation': violation.violation_number
			  }
			)
		print cheque
		time.sleep(3)
		#message = "Please text PAYCOURT to shortcode 77345 and we will reply with a confirmation once your payment is processed"
		message = twilio.twiml.Message("Thanks for paying your violation! Here is the cheque that we mailed out on your behalf.\n")
		message.media(cheque.thumbnails[0].large)
		resp.append(message)
		#resp.media(cheque.thumbnails[0].large)
		#with resp.message() as message:
			#message.body = "Thanks for paying your violation! Here is the cheque that we will mail out on your behalf\n"
			#message.media = cheque.thumbnails[0].large
		print message
		return resp
	else:
		message = "Sorry, we did not understand your command, please enter START to view the main menu.\n"

	resp.sms(message)
	print message
	return resp

def run():
	app.run(debug=True)


if __name__ == "__main__":
	app.run(debug=True)