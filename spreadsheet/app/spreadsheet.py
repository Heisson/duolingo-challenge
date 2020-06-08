import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from . import state

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_id = "11sCfPdirODppDGEa5bqAsUW6gO6A6oY4BXUpYlXtQOg"
# spreadsheet_id = "1iPQjZXCwfL58-z4FfjcQFDRn5YTuN5sYiUA3jxqAtJ8"
client_secrets_file = "credentials.json"
starting_row = 2
range_name = f"A{starting_row}:J"

def get_usernames(data):
	return [
		{"username": row[0][row[0].find("(")+1:row[0].find(")")]}
		for row in data
	]


def get_spreadsheet():
	print("Getting usernames from spreadsheet.")

	credentials = None
	if os.path.exists("token.pickle"):
		with open("token.pickle", "rb") as token:
			credentials = pickle.load(token)

	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
			credentials = flow.run_local_server(port=0)

		with open("token.pickle", "wb") as token:
			pickle.dump(credentials, token)

	spreadsheet = build("sheets", "v4", credentials=credentials)

	return spreadsheet


def get_data_from_spreadsheet():
	spreadsheet = get_spreadsheet()
	sheet = spreadsheet.spreadsheets()
	result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

	data = result.get("values", [])

	return data if data else None
	#
	# if not data:
	# 	print("No data found.")
	# 	return None
	# else:
	# 	return data

def update_spreadsheet():
	spreadsheet = get_spreadsheet()
	sheet = spreadsheet.spreadsheets()

	users = state.load()

	body = {
		'valueInputOption': 'RAW',
		'data': [
			{
				'range': f"D{starting_row}:D{starting_row+len(users)}",
				'values': [[user["total_streak"]] for user in users]
			},
			{
				'range': f"F{starting_row}:F{starting_row+len(users)}",
				'values': [[user["total_xp"]] for user in users]
			}
		]
	}
	result = spreadsheet.spreadsheets().values().batchUpdate(
		spreadsheetId=spreadsheet_id,
		body=body
	).execute()

	print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


def get_and_save_data():
	data = get_data_from_spreadsheet()
	users = get_usernames(data)
	state.save(users)


if __name__ == '__main__':
	pass
