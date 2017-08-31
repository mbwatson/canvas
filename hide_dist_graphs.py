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
# ...or pull from json config file
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
	# Gather courses for various current terms
	fallCourses = account.get_courses(per_page=500, enrollment_term_id=101)
	springCourses = account.get_courses(per_page=500, enrollment_term_id=105)
	yearlongCourses = account.get_courses(per_page=500, enrollment_term_id=120)
	# Combine all current courses into one list
	courses = list(chain(fallCourses, springCourses, yearlongCourses))
	# Iterate through each course, updating settings
	for course in courses:
		print(course.name + " ( " + str(course.id) + " )")
		# course.update_settings(hide_distribution_graphs="true")
		print("OK!")

