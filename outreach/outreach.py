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

def run():
	# while True:
		citations = Object.factory("citations")
		violations = Object.factory("violations")
		tomorrow_datetime = datetime.date.today() + datetime.timedelta(days=1)
		tomorrow = '{dt.month}/{dt.day}/{dt.year} 0:00'.format(dt = tomorrow_datetime)
		all_citations = citations.Query.all()#.filter(court_date=tomorrow)
		for citation in all_citations:
			try:
				if not citation.proactive_outreach:
					# print "reachout!"
					try:
						reachout_sms = "Hey! It's a reminder from ProactiveLaw that you have a court date tomorrow in " + citation.court_location + " at " + citation.court_address
						print reachout_sms
					except:
						print "no court date"
					citation.proactive_outreach = True;
					citation.save()
					# find the user with this citation
			except:
				print "reachout!"
				citation.proactive_outreach = True;
				citation.save()

   		all_violations = violations.Query.all() #.filter(status="FTA WARRANT ISSUED")
		for violation in all_violations:
   			try:
				if not violation.proactive_outreach:
					print "reachout!"
					violation.proactive_outreach = True;
					violation.save()
			except:
				print "reachout!"
				violation.proactive_outreach = True;
				violation.save()
		# time.sleep(15)


court_numbers = [
{"BALLWIN","(636) 227-9468"},
{"BELLA VILLA","(314) 638-8840"},
{"BELLEFONTAINE NEIGHBORS","(314) 867-0076"},
{"BELLERIVE","(314) 385-3300"},
{"BEL-NOR","(314) 381-2834"},
{"BEL-RIDGE","(314) 429-2878"},
{"BERKELEY","(314) 524-3313"},
{"BEVERLY HILLS","(314) 382-6544"},
{"BLACK JACK","(314) 355-0400"},
{"BRECKENRIDGE HILLS","(314) 427-1412"},
{"BRENTWOOD","num"},
{"BRIDGETON","num"},
{"CALVERTON PARK","num"},
{"CHAMP","num"},
{"CHARLACK","num"},
{"CHESTERFIELD","num"},
{"CLARKSON VALLEY","num"},
{"CLAYTON","num"},
{"COOL VALLEY","num"},
{"COUNTRY CLUB HILLS","num"},
{"COUNTRY LIFE ACRES","num"},
{"CRESTWOOD","num"},
{"CREVE COEUR","num"},
{"CRYSTAL LAKE PARK","num"},
{"DELLWOOD","num"},
{"DES PERES","num"},
{"EDMUNDSON","num"},
{"ELLISVILLE","num"},
{"EUREKA","num"},
{"FENTON","num"},
{"FERGUSON","num"},
{"FLORDELL HILLS","num"},
{"FLORISSANT","num"},
{"FRONTENAC","num"},
{"GLEN ECHO PARK","num"},
{"GLENDALE","num"},
{"GRANTWOOD VILLAGE","num"},
{"GREENDALE","num"},
{"GREEN PARK","num"},
{"HANLEY HILLS","num"},
{"HAZELWOOD","num"},
{"HILLSDALE","num"},
{"HUNTLEIGH","num"},
{"JENNINGS","num"},
{"KINLOCH","num"},
{"KIRKWOOD","num"},
{"LADUE","num"},
{"LAKESHIRE","num"},
{"MACKENZIE","num"},
{"MANCHESTER","num"},
{"MAPLEWOOD","num"},
{"MARLBOROUGH","num"},
{"MARYLAND HEIGHTS","num"},
{"MOLINE ACRES","num"},
{"NORMANDY","num"},
{"NORTHWOODS","num"},
{"NORWOOD COURT","num"},
{"OAKLAND","num"},
{"OLIVETTE","num"},
{"OVERLAND","num"},
{"PACIFIC","num"},
{"PAGEDALE","num"},
{"PASADENA HILLS","num"},
{"PASADENA PARK","num"},
{"PINE LAWN","num"},
{"RICHMOND HEIGHTS","num"},
{"RIVERVIEW","num"},
{"ROCK HILL","num"},
{"SHREWSBURY","num"},
{"ST. ANN","num"},
{"ST. JOHN","num"},
{"SUNSET HILLS","num"},
{"SYCAMORE HILLS","num"},
{"TOWN AND COUNTRY","num"},
{"TWIN OAKS","num"},
{"UNIVERSITY CITY","num"},
{"UPLANDS PARK","num"},
{"VALLEY PARK","num"},
{"VELDA CITY","num"},
{"VELDA VILLAGE HILLS","num"},
{"VINITA PARK","num"},
{"VINITA TERRACE","num"},
{"WARSON WOODS","num"},
{"WEBSTER GROVES","num"},
{"WELLSTON","num"},
{"WESTWOOD","num"},
{"WILBUR PARK","num"},
{"WILDWOOD","num"},
{"WINCHESTER","num"},
{"WOODSON TERRACE","num"},
{"UNINCORPORATED ST. LOUIS COUNTY","num"}
]
