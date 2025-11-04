from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle
import time
import re  

# Scope cho Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_asset(local_file_path: str, description: str = ""): 
    if not os.path.exists(local_file_path):
        print(f"[Drive] File không tồn tại: {local_file_path}")
        return None

    print(f"[Drive] Uploading asset from {local_file_path}")

    # TẠO TÊN FILE ĐỘC NHẤT
    if description:
        safe_desc = re.sub(r'[^\w\s-]', '', description).strip().lower()
        safe_desc = re.sub(r'\s+', '_', safe_desc)[:50]  # Giới hạn 50 ký tự
        timestamp = int(time.time())
        file_ext = os.path.splitext(local_file_path)[1]
        new_filename = f"{safe_desc}_{timestamp}{file_ext}"
    else:
        new_filename = os.path.basename(local_file_path)

    creds = None
    token_path = "token.pickle"
    creds_path = "oauth-credentials.json"

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"[Drive] Thiếu file: {creds_path}")
                print("   → Tạo OAuth Client ID tại: https://console.cloud.google.com/apis/credentials")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('drive', 'v3', credentials=creds)

        folder_id = os.getenv("GDRIVE_FOLDER_ID")
        file_metadata = {"name": new_filename}  
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(local_file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        web_link = file.get('webViewLink')

        # Chia sẻ công khai
        service.permissions().create(
            fileId=file.get('id'),
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()

        print(f"[Drive] Upload successful: {web_link}")
        return web_link

    except Exception as e:
        print(f"[Drive] Lỗi upload: {e}")
        return None