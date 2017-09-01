#!/usr/bin/python

from canvasapi import Canvas
import requests
import json

# terms
# 	courses
# 		observers
# 			channels *
# 				categories *

def get_observers_in_course(course):
	print(course.name)
	observers = course.get_users(enrollment="observer")
	print("\nObservers:\n")
	for observer in observers:
		print(" - " + observer.name + " (" + str(observer.id) + ")")
		user = canvas.get_user(observer.id)
		channels = user.list_communication_channels()
		for channel in channels:
			print("   " + str(channel.type) + ": " + str(channel))
			# print("   " + str(channel.__dict__))
		print();

with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}
preference = "never"

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	course = canvas.get_course(1819)
	print(course.name)
	observers = course.get_users(enrollment_type="observer")
	print("\nObservers:\n")
	for user in observers:
		###########################
		print("="*(len(user.name)))
		print(user.name)
		print("ID: " + str(user.id))
		print("="*(len(user.name)))
		###########################
		channels = user.list_communication_channels()
		for channel in channels:
			print("\n" + user.name + "  < " + str(channel) + " >\n")
			response = requests.get(API_URL + "users/{}/communication_channels/{}/notification_preference_categories".format(user.id, channel.id), headers = headers)
			categories = response.json()['categories']
			payload = { "notification_preferences": [ {"frequency": preference} ] }
			for category in categories:
				response = requests.put(API_URL + "users/self/communication_channels/{}/notification_preference_categories/{}?as_user_id={}".format(channel.id, category, user.id), headers = headers, json = payload)
				print("* Category " + category, end = "")
				if response.status_code == 200:
					print(" - OK, set to " + preference + "!")
				else:
					print("  * * * Error " + str(response.status_code) + " * * *")
	print()
