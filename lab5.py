import csv
from typing import Tuple


class ImagePathIterator:
    """Итератор для построчного чтения annotation.csv (absolute_path, relative_path)"""

    def __init__(self, path: str):
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            self.data = list(reader)
        self.idx = 0

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self) -> Tuple[str, str]:
        if self.idx >= len(self.data):
            raise StopIteration
        row = self.data[self.idx]
        self.idx += 1
        return row[0].strip(), row[1].strip()