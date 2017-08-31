#!/usr/bin/env python

# Import the Canvas class
from canvasapi import Canvas
from itertools import chain

import json
with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Production']['API_URL']
API_KEY = config['Production']['API_KEY']

# Attempt with entered credentials
print("\nAttempting to access {}".format(API_URL))
print("with API key {}...\n".format(API_KEY))

# Initialize a new Canvas object
try:
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print(" >> An error occurred!\n")
else:
	print("\n=== " + account.name + " ===\n")
	course = canvas.get_course(1819)
	print(course.name)
	observers = course.get_users()
	print("\nObservers:\n")
	for observer in observers:
		print(" - " + observer.name + " (" + str(observer.id) + ")")
		user = canvas.get_user(observer.id)
		channels = user.list_communication_channels()
		for channel in channels:
			print("   " + str(channel.type) + ": " + str(channel))
			# print("   " + str(channel.__dict__))
		print();
