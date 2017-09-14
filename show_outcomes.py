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
API_URL = config['Test']['API_URL']
API_KEY = config['Test']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}

def time_since(old_time):
    return time.time() - old_time

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	outcome_ids = [5420,5419,5418]
	# ,5417,5416,5422,5421,5423,5424,5425,5426,5435,5434,5433,5432,5431,5430,5429,5428,5427,5441,5451,5450,5449,5448,5447,5440,5439,5438,5446,5445,5444,5443,5442,5437,5436,5415,5414,5411,5412,5413,5405,5406,5407,5408,5409,5410]
	print("Initial check...")
	for outcome_id in outcome_ids:
		response = requests.get(API_URL + "outcomes/{}".format(outcome_id), headers = headers)
		outcome_title = response.json()['title']
		print(outcome_title)
		print("Vendor GUID: {}".format(response.json()['vendor_guid']))
		print("Points possible: {}".format(response.json()['points_possible']))
		print("Mastery points: {}".format(response.json()['mastery_points']))

		# # Make changes
		# payload = { "points_possible": 3, "mastery_points": 3, "vendor_guid": outcome_title}
		# response = requests.put(API_URL + "outcomes/{}".format(outcome_id), headers = headers, json = payload)

		# # Check changes
		# response = requests.get(API_URL + "outcomes/{}".format(outcome_id), headers = headers)
		# print(response.json()['title'])
		# print("Vendor GUID: {}".format(response.json()['vendor_guid']))
		# print("Points possible: {}".format(response.json()['points_possible']))
		# print("Mastery points: {}".format(response.json()['mastery_points']))
