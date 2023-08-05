import json
import easy_spreadsheet

with open('/Users/junyeongpark/Documents/keys/google_sheet_key.json', 'r') as fp:
    sheet_key = json.loads(fp.read())

def test_default():
    spreadsheet_id = '13Wz9X9-4ZUGoOZ_7KYv5nLfotWNV6gyRCOsCe4KuYDo'
    handler = easy_spreadsheet.EasySpreadsheet(sheet_key, spreadsheet_id)
    sheet = handler.get_easy_worksheet('Table History')
    # print(sheet.push())

    # print(handler.get_worksheet_titles())
    # print(handler.delete_worksheet('시트4'))
    
    # handler.refresh()
    # handler.reorder(['Table History', 'Default'])
