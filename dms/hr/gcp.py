from django.conf import settings

import pygsheets


class Sheet:

    service_file = settings.GCP_CREDENTIAL

    def __init__(self, sheet_key: str, service_file: str = None) -> None:
        service_file = service_file or self.service_file
        client = pygsheets.authorize(service_file=service_file)
        self.sheets = client.open_by_key(sheet_key)

    def get_sheet(self):
        return self.sheets.sheet1

    def rows(self, cols: int = -1) -> None:
        sheet = self.get_sheet()
        for row in sheet.get_all_values():
            yield row[:cols]
