import os
import json
import glob
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.settings import GoogleAuthSettings

def upload_excel_snapshots():
    creds = json.loads(os.environ["GDRIVE_SERVICE_KEY"])
    folder_id = os.environ["GDRIVE_FOLDER_ID"]

    # Setup pydrive2 authentication using service account JSON
    settings = GoogleAuthSettings()
    settings['client_config_backend'] = 'service'
    settings['service_config'] = creds

    gauth = GoogleAuth(settings=settings)
    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)

    files = glob.glob("snapshots/*/*.xlsx")
    if not files:
        print("⚠️ Keine Excel-Dateien gefunden – Upload übersprungen.")
        return

    for path in files:
        fname = os.path.basename(path)
        print(f"📤 Uploading: {fname}")
        gfile = drive.CreateFile({'title': fname, 'parents': [{'id': folder_id}]})
        gfile.SetContentFile(path)
        gfile.Upload()
        print(f"✅ Erfolgreich hochgeladen: {fname}")

if __name__ == "__main__":
    upload_excel_snapshots()
