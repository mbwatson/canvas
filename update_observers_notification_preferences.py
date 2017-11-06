#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json
import time
import sys

program_start_time = time.time()

# Read login credentials
with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}

# Ids of terms from which to gather courses and their observers
# Enter term_ids at program execution:
# "python3 update_observers_notification_preferences.py 101,105,120"
term_ids = sys.argv[1].split(',')

def time_since(old_time):
    return time.time() - old_time

def get_courses_by_term_ids(term_ids):
	courses = []
	for term_id in term_ids:
		courses = list(chain(courses, account.get_courses(per_page=500, enrollment_term_id=term_id)))
	return(courses)

def get_course_observer_ids(course):
	course_observer_ids = []
	course_observers = course.get_users(enrollment_type="observer")
	for observer in course_observers:
		course_observer_ids += [observer.id]
	return(course_observer_ids)

def update_user_notification_preferences(user, desired_preference):
	channels = user.list_communication_channels()
	for channel in channels:
		print("\n - " + str(channel) + "\n")
		response = requests.get(API_URL + "users/{}/communication_channels/{}/notification_preferences".format(user.id, channel.id), headers = headers)
		preferences = response.json()['notification_preferences']
		for preference in preferences:
			if str(preference['frequency']) != desired_preference:
				print("    - {}: '{}'".format(preference['notification'],preference['frequency']), end="")
				payload = { "notification_preferences": [ {"frequency": desired_preference} ] }
				response = requests.put(API_URL + "users/self/communication_channels/{}/notification_preferences/{}?as_user_id={}".format(channel.id, preference['notification'], user.id), headers = headers, json = payload)
				print(" => Changed to '{}'".format(desired_preference))

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
	print("Accessing Term IDs:")
	for term_id in term_ids:
		print(" " + str(term_id))
	print()
	courses = get_courses_by_term_ids(term_ids)
	print("Courses\n" + "="*60)
	# Loop through all the courses
	for course in courses:
		course_start_time = time.time()
		course_observer_ids = get_course_observer_ids(course)
		print("{} +{} observers".format(course.name,len(course_observer_ids)))
		all_observer_ids = all_observer_ids + course_observer_ids
	# Remove duplicates/convert to set
	all_observer_ids = set(all_observer_ids)
	observers_num = len(all_observer_ids)
	print("\n" + "="*60 + "\n Total: {} observers".format(observers_num) + "\n" + "="*60 + "\n")
	# Loop through all observers by ID
	observer_count = 0
	for id in all_observer_ids:
		user_start_time = time.time()
		user = canvas.get_user(id)
		observer_count += 1
		print()
		print("{} / {}".format(observer_count,observers_num), end="")
		print(" - {} (ID: {})\n".format(user.name,user.id) + "-"*60)
		update_user_notification_preferences(user, "never")
		print()
		print("User change time: {} seconds".format(time_since(user_start_time)))
		print("Total runtime: {} seconds".format(time_since(program_start_time)))
		print()
		print("="*60)
