#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json

with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}

user_id = 408

def update_user_notification_preferences(user, desired_preference):
	channels = user.list_communication_channels()
	for channel in channels:
		print("\n" + user.name + "  <" + str(channel) + ">\n")
		response = requests.get(API_URL + "users/{}/communication_channels/{}/notification_preferences".format(user.id, channel.id), headers = headers)
		preferences = response.json()['notification_preferences']
		for preference in preferences:
			print(str(preference['notification']) + " - " + str(preference['frequency']))
			if str(preference['frequency']) != desired_preference:
				payload = { "notification_preferences": [ {"frequency": desired_preference} ] }
				response = requests.put(API_URL + "users/self/communication_channels/{}/notification_preferences/{}?as_user_id={}".format(channel.id, preference['notification'], user.id), headers = headers, json = payload)
				print(" => changed to " + desired_preference)
			print()

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	user = canvas.get_user(user_id)
	update_user_notification_preferences(user, "immediately")