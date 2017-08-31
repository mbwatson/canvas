#!/usr/bin/env python

# Import the Canvas class
from canvasapi import Canvas
from itertools import chain

# Get Canvas API URL and Key from user...
print("\nWhat instance of Canvas ( _________.instructure.com ) ? ")
instance = input(" >> ")
API_URL = "https://{}.instructure.com/api/v1/".format(instance)
print("\nAPI KEY?")
API_KEY = input(" >> ")
# ...or hardcode this stuff
# sms
# API_URL = "https://sms.instructure.com/api/v1/"
# API_KEY = "2452~oFBYJxGFuMJk4iflxAi2OYVeElXDfnTAS8dbWe8hzISdc0wybIsGb8nWroVuxHAd"
# sms.beta
API_URL = "https://sms.beta.instructure.com/api/v1/"
API_KEY = "2452~1SelymsKG1Wr30iYMyqiV4qDpXuQp5nJi6o201SxrQJ5sI4RWYWZuWQfkhS1XQRm" # sms.beta

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
