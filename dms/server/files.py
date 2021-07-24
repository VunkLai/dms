import csv
from pathlib import Path


class File:

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def read(self):
        try:
            with self.path.open('r', encoding='big5') as fr:
                yield from fr
        except UnicodeDecodeError:
            # UTF8 with BOM
            with self.path.open('r', encoding='utf-8-sig') as fr:
                yield from fr


class CSVFile(File):

    def read(self):
        yield from csv.DictReader(super().read())
