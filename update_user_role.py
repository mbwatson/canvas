#!/usr/bin/python

from canvasapi import Canvas
from itertools import chain
import requests
import json

with open('config.json', 'r') as f:
  config = json.load(f)
API_URL = config['Beta']['API_URL']
API_KEY = config['Beta']['API_KEY']
headers = {
    'Content-type': 'application/json',
    'Authorization' : 'Bearer ' + API_KEY
}

account_id = 1
user_id = 408

try:
	# Attempt access with entered credentials
	print("\nAccessing {}".format(API_URL))
	print("with API key {}...\n".format(API_KEY))
	canvas = Canvas(API_URL, API_KEY)
	account = canvas.get_account(1);
except:
	print("An error occurred accessing the API!")
else:
	user = canvas.get_user(user_id)
	response = requests.get(API_URL + "accounts/{}/admins?per_page=100".format(account_id), headers = headers)
	admins = response.json()
	for admin in admins:
		print("{} ({}) - {} ({})".format(admin['user']['sortable_name'], admin['user']['id'], admin['role'], admin['role_id']))