import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_id = "11sCfPdirODppDGEa5bqAsUW6gO6A6oY4BXUpYlXtQOg"
client_secrets_file = "credentials.json"
range_name = "A2:J"

def get_data_from_spreadsheet():
	credentials = None

	if os.path.exists("token.pickle"):
		with open("token.pickle", "rb") as token:
			credentials = pickle.load(token)

	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
			credentials = flow.run_local_seer(port=0)

		with open("token.pickle", "wb") as token:
			pickle.dump(credentials, token)

	service = build("sheets", "v4", credentials=credentials)
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

	return result.get("values", [])

if __name__ == '__main__':
	get_data_from_spreadsheet()