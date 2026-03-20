from parsing import Parsing
import sys
from typing import List, Dict
from collections import deque


class Djikstra:
    def __init__(self) -> None:
        self.parser = Parsing()
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []
        self.path: List[Dict[str, int]] = [{}]

    def parse_file(self, file: str) -> None:
        self.parser.read_file(file)
        self.parser.check_line()
        self.parser.parse()
        self.start = self.parser.start
        self.end = self.parser.end
        self.path = self.parser.zones
        self.connection = self.parser.connections

    def get_path(self) -> None:
        visite = [self.start]
        parent = []
        queue = deque(self.start)
        while queue:
            current = queue.popleft()
            if current == self.end:
                break
            direction = deque()
            for i in self.parser.connections:
                if i[0] == current[0]:
                    direction.append(i[1])
            
            
            




if __name__ == "__main__":
    try:
        test = Djikstra()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.get_path()
    except Exception as e:
        print(e)
