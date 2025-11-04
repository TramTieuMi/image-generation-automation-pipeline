import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SHEET_KEY = os.getenv("SHEET_KEY")

def get_sheet_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    return service

def read_new_requests():
    service = get_sheet_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_KEY, range="Sheet1!A2:F").execute()#??????????????
    rows = result.get("values", [])

    headers = ["description", "example_asset_urls", "format", "model", "status", "asset_url"]
    pending = []

    for i, row in enumerate(rows):
        while len(row) < len(headers):
            row.append("")
        data = dict(zip(headers, row))
        if data["status"].lower() == "generate":
            data["row_index"] = i + 2
            pending.append(data)

    return pending

def update_status(row_index, asset_url):
    service = get_sheet_service()
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_KEY,
        range=f"Sheet1!E{row_index}:F{row_index}",
        valueInputOption="RAW",
        body={"values": [["done", asset_url]]}
    ).execute()
