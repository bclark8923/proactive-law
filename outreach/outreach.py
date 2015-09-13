# -*- coding: utf-8 -*-
#! /usr/bin/env python
import sys
import string
import httplib
import json
import time
import datetime
import threading
import errno
import os
from parse_rest.datatypes import Object
from twilio.rest import TwilioRestClient

account_sid = "AC5e947e28bfef48a9859c33fec7278ee8"
auth_token  = "02c707399042a867303928beb261e990"
client = TwilioRestClient(account_sid, auth_token)

def run():
	while True:
		try: 
			citations = Object.factory("citations")
			violations = Object.factory("violations")
			users = Object.factory("user")
			# violations = Object.factory("violations")
			tomorrow_datetime = datetime.date.today() + datetime.timedelta(days=1)
			tomorrow = '{dt.month}/{dt.day}/{dt.year} 0:00:00'.format(dt = tomorrow_datetime)
			tomorrows_citations = citations.Query.filter(court_date=tomorrow,proactive_outreach=False)
			for citation in tomorrows_citations:
				try:
					user = users.Query.get(first_name=citation.first_name,last_name=citation.last_name,birthdate=citation.date_of_birth)
					reachout_sms = "Hey! It's a reminder from ProactiveLaw that you have a court date tomorrow in " + citation.court_location + " at " + citation.court_address + " to get more information call them at " + court_numbers[citation.court_location]
					message = client.messages.create(body=reachout_sms,
					    to=user.phone_number,    # Replace with your phone number
					    from_="+13142549337") # Replace with your Twilio number
					# print message.sid
					citation.proactive_outreach = True;
					citation.save()
				except:
					print "No court date or not enough information"

	   		warrant_violations = violations.Query.filter(status="FTA WARRANT ISSUED",proactive_outreach=False)
			for violation in warrant_violations:
	   			try:
	   				citation = citations.Query.get(citation_number=violation.citation_number)
					user = users.Query.get(first_name=citation.first_name,last_name=citation.last_name,birthdate=citation.date_of_birth)
					amount_owed = violation.fine_amount + violation.court_cost
					reachout_sms = "Hey! It's a notification from ProactiveLaw that a warrant " + violation.warrant_number + " has been issued for your arrest for violation: " + violation.violation_number + " " + violation.violation_description + ", you owe $" + str(amount_owed) + " to the court " + citation.court_location + " at " + citation.court_address + " to get more information call them at " + court_numbers[citation.court_location] + ". To Pay now respond with PAY " + violation.violation_number
					message = client.messages.create(body=reachout_sms,
					    to=user.phone_number,    # Replace with your phone number
					    from_="+13142549337") # Replace with your Twilio number
					violation.proactive_outreach = True;
					violation.save()
				except:
					print "No court date or not enough information"

			payment_violations = violations.Query.filter(status="CONT FOR PAYMENT",proactive_outreach=False)
			for violation in payment_violations:
	   			try:
	   				citation = citations.Query.get(citation_number=violation.citation_number)
					user = users.Query.get(first_name=citation.first_name,last_name=citation.last_name,birthdate=citation.date_of_birth)
					amount_owed = violation.fine_amount + violation.court_cost
					reachout_sms = "Hey! It's a notification from ProactiveLaw that a payment is owed for violation: " + violation.violation_number + " " + violation.violation_description + ", you owe $" + str(amount_owed) + " to the court " + citation.court_location + " at " + citation.court_address + " to get more information call them at " + court_numbers[citation.court_location] + ". To Pay now respond with PAY " + violation.violation_number

					message = client.messages.create(body=reachout_sms,
					    to=user.phone_number,    # Replace with your phone number
					    from_="+13142549337") # Replace with your Twilio number
					violation.proactive_outreach = True;
					violation.save()
				except:
					print "No court date or not enough information"
			# sys.exit(0)
		except: 
			print "error"
		time.sleep(5)

court_numbers = {
"BALLWIN":"(636) 227-9468",
"BEL-NOR":"(314) 381-2834",
"BEL-RIDGE":"(314) 429-2878",
"BELLA VILLA":"(314) 638-8840",
"BELLEFONTAINE NEIGHBORS":"(314) 867-0076",
"BERKELEY":"(314) 524-3313",
"BEVERLY HILLS":"(314) 382-6544",
"BLACK JACK":"(314) 355-0400",
"BRECKENRIDGE HILLS":"(314) 427-1412",
"BRENTWOOD":"(314) 963-8621",
"BRIDGETON":"(314) 739-1145",
"CALVERTON PARK":"(314) 524-1212",
"CHARLACK":"(314) 427-4715",
"CHESTERFIELD":"(636) 537-4718",
"CLARKSON VALLEY":"(636) 227-8607",
"CLAYTON":"(314) 290-8441",
"COOL VALLEY":"(314) 521-3500",
"COUNTRY CLUB HILLS":"(314) 261-0845",
"CRESTWOOD":"(314) 729-4776",
"CREVE COEUR":"(314) 432-8844",
"DELLWOOD":"(314) 521-4339",
"DES PERES":"(314) 835-6117",
"EDMUNDSON":"(314) 428-7125",
"ELLISVILLE":"(636) 227-3729",
"EUREKA":"(636) 938-6600",
"FENTON":"(636) 343-1007",
"FERGUSON":"(314) 524-5264",
"FLORDELL HILLS":"(314) 382-5524",
"FLORISSANT":"(314) 921-3322",
"FRONTENAC":"(314) 994-3204",
"GLENDALE":"(314) 965-0000",
"GRANTWOOD VILLAGE":"(314) 842-4409",
"GREENDALE":"(314) 385-3300",
"HANLEY HILLS":"(314) 725-0909",
"HAZELWOOD":"(314) 839-2212",
"HILLSDALE":"(314) 381-0288",
"JENNINGS":"(314) 385-4670",
"KINLOCH":"(314) 521-3335",
"KIRKWOOD":"(314) 822-5840",
"LADUE":"(314) 993-3919",
"LAKESHIRE":"(314) 631-6222",
"MACKENZIE":"(314) 752-0625",
"MANCHESTER":"(636) 227-1385",
"MAPLEWOOD":"(314) 646-3636",
"MARLBOROUGH":"(314) 962-5055",
"MARYLAND HEIGHTS":"(314) 291-6036",
"MOLINE ACRES":"(314) 868-2433",
"NORMANDY":"(314) 385-3300",
"NORTHWOODS":"(314) 385-0260",
"OAKLAND":"(314) 842-0778",
"OLIVETTE":"(314) 991-6047",
"OVERLAND":"(314) 428-1224",
"PACIFIC":"(636) 257-4553",
"PAGEDALE":"(314) 726-1200",
"PASADENA HILLS":"(314) 382-4453",
"PASADENA PARK":"(314) 385-4115",
"PINE LAWN":"(314) 802-1043",
"RICHMOND HEIGHTS":"(314) 645-1982",
"RIVERVIEW":"(314) 868-0700",
"ROCK HILL":"(314) 962-6265",
"SHREWSBURY":"(314) 647-8634",
"ST. ANN":"(314) 428-6811",
"ST. JOHN":"(314) 427-8700",
"SUNSET HILLS":"(314) 849-3402",
"SYCAMORE HILLS":"(314) 427-8700",
"TOWN AND COUNTRY":"(314) 432-6606",
"TWIN OAKS":"(314) 615-5000",
"UNIVERSITY CITY":"(314) 505-8578",
"VALLEY PARK":"(636) 225-5696",
"VELDA CITY":"(314) 382-6600",
"VELDA VILLAGE HILLS":"(314) 261-7221",
"VINITA PARK":"(314) 428-7373",
"VINITA TERRACE":"(314) 427-4488",
"WARSON WOODS":"(314) 965-3100",
"WEBSTER GROVES":"(314) 963-5416",
"WELLSTON":"(314) 553-8002",
"WILDWOOD":"(636) 458-8277",
"WINCHESTER":"(636) 391-0600",
"WOODSON TERRACE":"(314) 427-2600",
}
