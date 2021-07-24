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
            with self.path.open('r', encoding='utf8') as fr:
                yield from fr

    def csv(self):
        pass
