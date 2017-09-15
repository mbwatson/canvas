#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json
import time
import sys

outcome_ids = [5420,5419,5418,5417,5416,5422]
# ,5421,5423,5424,5425,5426,5435,5434,5433,5432,5431,5430,5429,5428,5427,5441,5451,5450,5449,5448,5447,5440,5439,5438,5446,5445,5444,5443,5442,5437,5436,5415,5414,5411,5412,5413,5405,5406,5407,5408,5409,5410]

def time_since(old_time):
    return time.time() - old_time

class Outcome():
	def __init__(self, outcome_id, outcome_title):
		self.id = outcome_id
		self.title = outcome_title

	def __str__(self):
		return "{}".format(self.title)

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

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	outcomes = []
	for outcome_id in outcome_ids:
		response = requests.get(API_URL + "outcomes/{}".format(outcome_id), headers = headers)
		outcome = Outcome(outcome_id, response.json()['title'])
		outcomes.append(outcome)
		# print(outcome.title)
	print("Outcomes loaded.")
	course = canvas.get_course(1875)
	print(course.name)
	students = course.get_users(enrollment_type="student")
	for student in students:
		print(student.name)
		for outcome in outcomes:
			response = requests.get(API_URL + "courses/{}/outcome_results?user_ids[]={}".format(course.id, student.id), headers = headers)
			print("  {}".format(outcome))
			outcome_results = response.json()['outcome_results']
			print(outcome_results)