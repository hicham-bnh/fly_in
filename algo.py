from parsing import Parsing
import sys
from typing import List, Dict


class Djikstra:
    def __init__(self) -> None:
        self.parser = Parsing()
        self.start: List[tuple[int, int]] = []
        self.end: List[tuple[int, int]] = []
        self.path: List[Dict[str, int]] = [{}]

    def parse_file(self, file: str) -> None:
        self.parser.read_file(file)
        self.parser.check_line()
        self.parser.parse()
        self.start = self.parser.start
        self.end = self.parser.end
        self.path = self.parser.zones

    def get_path(self) -> None:
        ...


if __name__ == "__main__":
    try:
        test = Djikstra()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.get_path()
    except Exception as e:
        print(e)
