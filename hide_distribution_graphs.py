#!/usr/bin/env python

# Import the Canvas class
from canvasapi import Canvas
from itertools import chain

def get_courses_by_term_ids(idList):
	# Grab courses
	courses = []
	for termId in idList:
		courses = list(chain(courses, account.get_courses(per_page=500, enrollment_term_id=termId)))
	return(courses)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Pull credentials from json config file
import json
with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
# ...or prompt user for Canvas API URL and Key.
# print("\nEnter your Canvas URL ( _________.instructure.com ) : ")
# instance = input(" >> ")
# API_URL = "https://{}.instructure.com/api/v1/".format(instance)
# print("\nAPI KEY : ")
# API_KEY = input(" >> ")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
	print("\n=== {} ===\n".format(account.name))
	courses = get_courses_by_term_ids([101, 105, 120])
	# Iterate through each course, updating settings
	for course in courses:
		print("{} (id={}, term_id={})".format(course.name,course.id,course.enrollment_term_id))
		course.update_settings(hide_distribution_graphs="true")
		print("OK!")

