#!/usr/bin/env python

# Import the Canvas class
from canvasapi import Canvas
from itertools import chain
import json
with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Production']['API_URL']
API_KEY = config['Production']['API_KEY']

# Attempt with entered credentials
print("\nAttempting to access {}".format(API_URL))
print("with API key {}...\n".format(API_KEY))

def get_courses_by_term_ids(idList):
	# Grab courses
	courses = []
	for termId in idList:
		courses = list(chain(courses, account.get_courses(per_page=500, enrollment_term_id=termId)))
	return(courses)

# Initialize a new Canvas object
try:
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1)
except:
	print(" >> An error occurred!\n")
else:
	print("\n=== " + account.name + " ===\n")
	courses = get_courses_by_term_ids([101, 105, 120])
	for c in courses:
		print(c.name)
		print(c.enrollment_term_id)