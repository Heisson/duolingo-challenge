values = [
    [
        # Cell values ...
    ],
    # Additional rows
]
data = [
    {
        'range': range_name,
        'values': values
    },
    # Additional ranges to update ...
]
body = {
    'valueInputOption': value_input_option,
    'data': data
}
result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id, body=body).execute()
print('{0} cells updated.'.format(result.get('totalUpdatedCells')))