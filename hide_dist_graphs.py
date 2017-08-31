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
# API_URL = "https://sms.instructure.com/api/v1/"
# API_KEY = "2452~oFBYJxGFuMJk4iflxAi2OYVeElXDfnTAS8dbWe8hzISdc0wybIsGb8nWroVuxHAd"

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

	fallCourses = account.get_courses(per_page=500, enrollment_term_id=101)
	springCourses = account.get_courses(per_page=500, enrollment_term_id=105)
	yearlongCourses = account.get_courses(per_page=500, enrollment_term_id=120)
	# Combine all current term courses
	courses = list(chain(fallCourses, springCourses, yearlongCourses))

	for course in courses:
		print(course.name + " ( " + str(course.id) + " )")
		# course.update_settings(hide_distribution_graphs="true")
		print("ok.")
		


