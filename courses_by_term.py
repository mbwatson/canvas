#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json
import time

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
current_term_ids = [1, 101, 105, 120] # IDs of terms from which to gather obervers

def get_courses_by_term_ids(term_ids):
	courses = []
	for termId in term_ids:
		courses = list(chain(courses, account.get_courses(per_page=500, enrollment_term_id=termId)))
	return(courses)

def get_terms():
	terms = []
	response = requests.get(API_URL + "accounts/{}/terms".format(account.id), headers = headers)
	return response.json()['enrollment_terms']

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	terms = get_terms()
	concluded_term_ids = []
	for term in terms:
		print("{} - {}".format(str(term['name']), str(term['id'])))
		if not term['id'] in current_term_ids:
			concluded_term_ids.append(term['id'])
	print(concluded_term_ids)
