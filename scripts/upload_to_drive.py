import os, json, glob
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_excel_snapshots():
    creds_json = json.loads(os.environ["GDRIVE_SERVICE_KEY"])
    folder_id = os.environ["GDRIVE_FOLDER_ID"]

    creds = service_account.Credentials.from_service_account_info(
        creds_json,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    # 🧭 Prüfen, ob Ordner erreichbar ist
    try:
        folder_info = service.files().get(fileId=folder_id, fields="id, name, driveId").execute()
        print(f"📁 Zielordner: {folder_info['name']} ({folder_info['id']})")
        drive_id = folder_info.get("driveId")  # None, wenn kein Shared Drive
    except Exception as e:
        raise RuntimeError(f"⚠️ Ungültige oder nicht freigegebene Folder-ID: {e}")

    # 📄 Alle Snapshots finden
    files = glob.glob("snapshots/*/*.xlsx")
    if not files:
        print("⚠️ Keine Snapshot-Dateien gefunden.")
        return

    for path in files:
        fname = os.path.basename(path)
        print(f"📤 Uploading: {fname}")

        file_metadata = {"name": fname, "parents": [folder_id]}
        media = MediaFileUpload(
            path,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            resumable=True
        )

        try:
            res = service.files().create(
                body=file_metadata,
                media_body=media,
                supportsAllDrives=True,
                fields="id, name, parents"
            ).execute()
            print(f"✅ Erfolgreich hochgeladen: {res['name']} (ID: {res['id']})")
        except Exception as e:
            print(f"❌ Fehler beim Upload {fname}: {e}")

if __name__ == "__main__":
    upload_excel_snapshots()
