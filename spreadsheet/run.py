import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from requests_html import HTML, HTMLSession

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_id = "11sCfPdirODppDGEa5bqAsUW6gO6A6oY4BXUpYlXtQOg"
# spreadsheet_id = "1iPQjZXCwfL58-z4FfjcQFDRn5YTuN5sYiUA3jxqAtJ8"
client_secrets_file = "credentials.json"
starting_row = 2
range_name = f"A{starting_row}:J"


def get_spreadsheet():
	print("Getting spreadsheet.")

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


def get_usernames():
	sheet = get_spreadsheet().spreadsheets()

	result = sheet.values().get(
		spreadsheetId=spreadsheet_id,
		range=range_name
	).execute()

	data = result.get("values", [])

	return [
		{"username": row[0][row[0].find("(")+1:row[0].find(")")]}
		for row in data
	]


def update_spreadsheet(users):
	spreadsheet = get_spreadsheet()
	sheet = spreadsheet.spreadsheets()

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

	print(f"Done. {result.get('totalUpdatedCells')} cells updated.")


def get_users_info(users):
	for user_index, user in enumerate(users):
		username = user["username"]

		response_html = HTMLSession().get(
			f"http://duome.eu/{username}",
			headers={"Cookie": f"PHPSESSID=4dfcaa82cc994ccc6b18d5f906a197bd",},
		).html

		streak = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]", first=True).text
		if "#" in streak:
			streak = response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[3]/span[1]", first=True).text

		users[user_index] = {
			"username": username,
			"total_xp": response_html.xpath("/html/body/div[2]/div[1]/div[3]/h2/span[1]", first=True).text.replace(" XP", ""),
			"total_streak": streak
		}

		print(f"Getting info from duome.eu ({(100*(user_index+1)/len(users)):.1f}% complete)")

	return users


if __name__ == '__main__':
	users = get_usernames()
	users = get_users_info(users)
	update_spreadsheet(users)
