#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json
import time

program_start_time = time.time()

with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}

term_ids = [101, 105, 120] # IDs of terms from which to gather obervers

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
			if str(preference['frequency']) != desired_preference:
				print(" - " + str(preference['notification']) + ": '" + str(preference['frequency']) + "'", end="")
				payload = { "notification_preferences": [ {"frequency": desired_preference} ] }
				response = requests.put(API_URL + "users/self/communication_channels/{}/notification_preferences/{}?as_user_id={}".format(channel.id, preference['notification'], user.id), headers = headers, json = payload)
				print(" => Changed to '" + desired_preference + "'")
try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	all_observer_ids = []
	courses = get_courses_by_term_ids(term_ids)
	print("Courses")
	print("=======")
	# Loop through all the courses
	for course in courses:
		course_observer_ids = []
		course_start_time = time.time()
		course_observers = course.get_users(enrollment_type="observer")
		for observer in course_observers:
			course_observer_ids += [observer.id]
		print(course.name + " + " + str(len(course_observer_ids)) + " observers")
		all_observer_ids = all_observer_ids + course_observer_ids
	# Remove duplicates
	all_observer_ids = set(all_observer_ids)
	print("\n" + "="*40 + "\n Total: {} observers".format(len(all_observer_ids)) + "\n" + "="*40 + "\n")
	# Loop through all observers by ID
	for id in all_observer_ids:
		user_start_time = time.time()
		user = canvas.get_user(id)
		print("\n" + user.name + " (ID: " + str(user.id) + ")\n" + "-"*40)
		update_user_notification_preferences(user, "never")
		print("\nUser change time: {} seconds".format(time.time() - user_start_time))
	print("\nTotal program runtime: {} seconds".format(time.time() - program_start_time))
