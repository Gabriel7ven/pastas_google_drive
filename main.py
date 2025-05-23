import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
# FOLDER_ID = '0B__gauNJE4aMQTB0aWZtekxsZHc'
FOLDER_ID = '12UY4vuSNsvpKa1hU8lMI9tuCxDTqQdI1'
query = f"'{FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder'"


def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(q=query,
            pageSize=500,
            fields="nextPageToken, files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
            )
        .execute()
    )
    items = results.get("files", [])

    # Exibe as pastas encontradas
    if not items:
        print("Nenhuma pasta encontrada.")
    else:
        print("Pastas encontradas:")
        for item in items:
            #print(f"ID: {item['id']}, Nome: {item['name']}")
            # print(f'{item['name']} https://drive.google.com/drive/folders/{item['id']}?hl=pt-br')
            print(item['name'])

        print(len(items))
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()