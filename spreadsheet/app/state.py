import json

def save(users):
	print("Saving data locally.")
	with open('users.json', 'w') as content_json:
		json.dump(users, content_json, indent=2)

def load():
	print("Loading data from local file.")
	with open('users.json') as json_file:
		return json.load(json_file)