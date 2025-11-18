import os
import json
import glob
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from tempfile import NamedTemporaryFile

def upload_excel_snapshots():
    # Secrets laden
    creds = json.loads(os.environ["GDRIVE_SERVICE_KEY"])
    folder_id = os.environ["GDRIVE_FOLDER_ID"]

    # Temporäre JSON-Datei für Credentials erzeugen
    with NamedTemporaryFile("w", delete=False, suffix=".json") as temp:
        json.dump(creds, temp)
        temp_path = temp.name

    try:
        # Authentifizierung über Service Account
        gauth = GoogleAuth()
        gauth.LoadServiceConfigSettings()
        gauth.LoadCredentialsFile(temp_path)
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

    finally:
        os.remove(temp_path)

if __name__ == "__main__":
    upload_excel_snapshots()
