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

def signup():
	while True:
		print "signup"
		time.sleep(15)