#!/usr/bin/env python
from canvasapi import Canvas
from itertools import chain
import sys

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pull credentials from json config file
import json
with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Production']['API_URL']
API_KEY = config['Production']['API_KEY']
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

course_id = sys.argv[1]

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
	course = canvas.get_course(course_id)
	print(course)
	students = course.get_users(enrollment_type='student')
	observers = course.get_users(enrollment_type='observer')

	print()
	
	print('Students:')
	for user in students:
		profile = user.get_profile()
		name = profile['name']
		email = profile['login_id']
		print('{}\t{}'.format(name, email))
	
	print()

	print('Observers:')
	for user in observers:
		profile = user.get_profile()
		name = profile['name']
		email = profile['login_id']
		print('{}\t{}'.format(name, email))
		user.list_observees()