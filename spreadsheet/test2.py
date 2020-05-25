from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_id = "11sCfPdirODppDGEa5bqAsUW6gO6A6oY4BXUpYlXtQOg"
client_secrets_file = "credentials.json"
range_name = "A1:A23"

def main():
	credentials = None

	if os.path.exists("token.pickle"):
		with open("token.pickle", "rb") as token:
			credentials = pickle.load(token)

	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refrech(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
			credentials = flow.run_local_server(port=0)
		with open("token.pickle", "wb") as token:
			pickle.dump(credentials, token)

	service = build("sheets", "v4", credentials=credentials)
	sheet = service.spreadsheets()
	result = sheet.values().get(
		spreadsheetId=spreadsheet_id,
		range=range_name
		).execute()
	values = result.get("values", [])

	print(values)


if __name__ == '__main__':
	main()