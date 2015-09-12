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
import signup
import outreach
import responder
from parse_rest.connection import register

if __name__ == '__main__':
	register("vvMc0yrmqU1kbU2nOieYTQGV0QzzfVQg4kHhQWWL", "waZK2MtE4TMszpU0mYSbkB9VmgLdLxfYf8XCuN7D", master_key="YPyRj37OFlUjHmmpE8YY3pfbZs7FqnBngxX4tezk")
	print "started"
	outreach.run()