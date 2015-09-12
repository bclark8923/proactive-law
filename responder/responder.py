# -*- coding: utf-8 -*-
#! /usr/bin/env python
import sys
import string
import httplib
import json
import time
import threading
import errno
import os

def run():
	while True:
		print "responder"
		time.sleep(15)