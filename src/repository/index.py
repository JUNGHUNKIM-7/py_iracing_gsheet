from datetime import datetime

import os.path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.model.index import O, Mapper, Result


class Repository:
    def __init__(self) -> None:
        self.options = O

    def read(self, sheetId: str) -> Result | None:
        creds = self.get_credential()
        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=sheetId,
                                        range=self.options.SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                return

            """
            A1
            |+++|
            |+++|E2

            => A1:E2
            """
            # [['1', '1', '3', '4', '5'], ['1', '2', '3', '4', '5']]
            # A1 = cols
            # others = rows
            cols, rows = values[0], values[1:]
            assert len(cols[0]) != len(
                rows[0]), "row and col are not matched: check googlesheet on web"
            assert len(cols) > 0 and len(
                rows), "cols and rows should be more than 0 len"
            return Mapper.new({
                "cols": cols,
                "rows": rows,
                "created": datetime.today()
            })
        except HttpError as err:
            raise Exception(err)

    def write(self, m: Result):
        """
            Creates the batch_update the user has access to.
            Load pre-authorized user credentials from the environment.
            TODO(developer) - See https://developers.google.com/identity
            for guides on implementing OAuth2 for the application.
        """
        # pylint: disable=maybe-no-member
        creds = self.get_credential()
        try:
            service = build('sheets', 'v4', credentials=creds)

            # Additional rows
            if m.rows is not None and m.cols is not None:
                len_of_rows = len(m.rows[0].vals)
                len_of_cols = len(m.cols[0])
                assert len_of_rows != len_of_cols, "len of rows & cols are not matched"

                O.SAMPLE_RANGE_NAME = f'A1:{chr(65+len_of_rows-1)}{len_of_rows}'
                shuoldUpdate = [(r.vals) for r in m.rows]
                cols_plus_rows = [m.cols, *shuoldUpdate]

            # Additional ranges to update ...
                data = [
                    {
                        'range': O.SAMPLE_RANGE_NAME,
                        'values': cols_plus_rows
                    },
                ]

                body = {
                    'valueInputOption': "USER_ENTERED",  # todo
                    'data': data
                }
                service.spreadsheets().values().batchUpdate(
                    spreadsheetId=O.SAMPLE_SPREADSHEET_ID, body=body).execute()
                return
        except HttpError as error:
            raise Exception(error)

    def create_sheet(self, title: str):
        """
        Creates the Sheet the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        creds = self.get_credential()
        # pylint: disable=maybe-no-member
        try:
            service = build('sheets', 'v4', credentials=creds)
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                        fields='spreadsheetId') \
                .execute()
            # Set google sheet ID here!
            O.SAMPLE_SPREADSHEET_ID = spreadsheet.get('spreadsheetId')
            # print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        except HttpError as error:
            raise Exception(error)

    def get_credential(self) -> Any:
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file(
                'token.json', self.options.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.options.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
