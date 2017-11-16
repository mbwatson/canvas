#!/usr/bin/env python

# Import the Canvas class
from canvasapi import Canvas
from itertools import chain

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pull credentials from json config file
import json
with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
# ...or prompt user for Canvas API URL and Key.
# print("\nEnter your Canvas ( _________.instructure.com ) : ")
# instance = input(" >> ")
# API_URL = "https://{}.instructure.com/api/v1/".format(instance)
# print("\nAPI KEY : ")
# API_KEY = input(" >> ")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	# Initialize a new Canvas object
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	count = 0
	users = account.get_users()
	print("\nUsers:\n")
	for user in users:
		if len(list(user.get_page_views(start_time="2017-08-01", end_time="2017-09-01"))):
			if ("@sms.edu" in user.login_id):
				print("{} < {} > ".format(user.name, user.login_id))
				count += 1
	print(count)
