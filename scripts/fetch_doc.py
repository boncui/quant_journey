import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials(
    None,
    refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
)

drive = build("drive", "v3", credentials=creds)
data = drive.files().export(
    fileId=os.environ["DOC_ID"], mimeType="text/markdown"
).execute()

with open("doc.md", "wb") as f:
    f.write(data)
print("wrote doc.md", len(data), "bytes")
