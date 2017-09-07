#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json

# terms
# 	courses
# 		observers
# 			channels *
# 				categories *

with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}

def get_courses_by_term_ids(idList):
	# Grab courses
	courses = []
	for termId in idList:
		courses = list(chain(courses, account.get_courses(per_page=500, enrollment_term_id=termId)))
	return(courses)

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
		print()

def update_user_notification_preferences(user, desired_preference):
	channels = user.list_communication_channels()
	for channel in channels:
		print("\n" + str(channel) + "\n")
		response = requests.get(API_URL + "users/{}/communication_channels/{}/notification_preferences".format(user.id, channel.id), headers = headers)
		preferences = response.json()['notification_preferences']
		for preference in preferences:
			print(" - " + str(preference['notification']) + ": '" + str(preference['frequency']) + "'", end="")
			if str(preference['frequency']) != desired_preference:
				payload = { "notification_preferences": [ {"frequency": desired_preference} ] }
				response = requests.put(API_URL + "users/self/communication_channels/{}/notification_preferences/{}?as_user_id={}".format(channel.id, preference['notification'], user.id), headers = headers, json = payload)
				print(" => Changed to '" + desired_preference + "'")
			else:
				print(" OK!")

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	courses = get_courses_by_term_ids([101, 105, 120])
	course = canvas.get_course(1819)
	for course in courses:
		print(course.name)
		print("="*(len(course.name)))
		observers = course.get_users(enrollment_type="observer")
		print("\nObservers in " + course.name + ":\n")
		for user in observers:
			print(user.name)
		print()
		for user in observers:
			###########################
			print()
			print(user.name + "(ID: " + str(user.id) + ")")
			print("="*40)
			###########################
			update_user_notification_preferences(user, "never")
		print()
