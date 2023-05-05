"""Api."""

import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def get_links_from_spreadsheet(id: str, token_name: str) -> list:
    """Should get a list of strings from the first column of a Google Spreadsheet with the given ID."""
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_name):
        with open(token_name, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id,
                                range='A:A').execute()
    values = result.get('values', [])

    links = []
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        links.append(row[0])
    return links


def get_links_from_playlist(link: str, developer_key: str) -> list:
    """Should get a list of links to songs in the Youtube playlist with the given address."""
    youtube = build('youtube', 'v3', developerKey=developer_key)
    playlists = youtube.playlistItems()

    items = playlists.list(
        part="snippet",
        playlistId=link.split("?list=")[1],
        maxResults=50
    ).execute()['items']

    ids = [x['snippet']['resourceId']['videoId'] for x in items]
    links = ['https://www.youtube.com/watch?v=' + x for x in ids]

    return links


if __name__ == '__main__':
    # print(get_links_from_spreadsheet('1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms', 'token.pickle'))
    pass
