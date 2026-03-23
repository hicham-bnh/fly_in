from parsing import Parsing
from typing import List, Optional, Dict
from collections import deque
import sys


class BFS:
    def __init__(self) -> None:
        self.parser = Parsing()
        self.start: List[tuple[str, int, int]] = []
        self.end: List[tuple[str, int, int]] = []
        self.path: List[str] = []
        self.adj = {}

    def parse_file(self, file: str) -> None:
        self.parser.read_file(file)
        self.parser.check_line()
        self.parser.parse()
        self.parser.check_start_end()
        self.start = self.parser.start
        self.end = self.parser.end
        self.connection = self.parser.connections
        self.adj = self.build_adj()

    def build_adj(self):
        adj = {}
        for zone in self.parser.zones:
            adj[zone['name']] = []
        for z1, z2 in self.parser.connections:
            name1 = z1['name']
            nmae2 = z2['name']
            adj[name1].append(z2)
            adj[nmae2].append(z1)
        return adj

    def get_test



if __name__ == "__main__":
    try:
        test = BFS()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.get_path_drone()
    except Exception as e:
        print(e)