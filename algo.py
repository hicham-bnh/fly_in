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
        self.connection = self.parser.connections

    def get_path(self) -> None:
        visite = []
        parent = []
        queue = deque(self.start)
        while queue:
            current = queue.popleft()
            visite.append(current)
            if current == self.end:
                break
            direction = deque()
            for i in self.parser.connections:
                if i[0]['name'] == current[0]:
                    if i[0].get('zone') != "blocked":
                        direction.append(i[1])
                directions =sorted(direction, key=lambda x: x['zone'] == 'priority')
        print(direction)
            
            




if __name__ == "__main__":
    try:
        test = Djikstra()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.get_path()
    except Exception as e:
        print(e)
