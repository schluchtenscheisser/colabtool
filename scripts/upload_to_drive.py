import os
import json
import glob
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_excel_snapshots():
    # Secrets laden
    creds_json = json.loads(os.environ["GDRIVE_SERVICE_KEY"])
    folder_id = os.environ["GDRIVE_FOLDER_ID"]

    # Authentifizierung
    creds = service_account.Credentials.from_service_account_info(
        creds_json,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build("drive", "v3", credentials=creds)

    # Alle Excel-Dateien finden
    files = glob.glob("snapshots/*/*.xlsx")
    if not files:
        print("⚠️ Keine Excel-Dateien gefunden – Upload übersprungen.")
        return

    for path in files:
        fname = os.path.basename(path)
        file_metadata = {"name": fname, "parents": [folder_id]}
        media = MediaFileUpload(path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        print(f"📤 Uploading: {fname}")
        uploaded = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"✅ Erfolgreich hochgeladen: {fname} (File ID: {uploaded.get('id')})")

if __name__ == "__main__":
    upload_excel_snapshots()
