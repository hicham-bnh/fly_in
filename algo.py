from parsing import Parsing
import sys
from typing import List, Dict
from collections import deque


class BFS:
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

    def get_path(self) -> None:
        start_node = self.start[0][0]
        end_node = self.end[0][0]
        queue = deque([start_node])
        visited = {start_node}
        parent = {}
        while queue:
            current = queue.popleft()
            if current == end_node:
                break
            voisin = self.build_adj()[current]
            for v in voisin:
                name_v = v['name']
                if name_v not in visited:
                    if v.get('zone') != "blocked":
                        visited.add(name_v)
                        parent[name_v] = current
                        queue.append(name_v)
        if end_node not in parent and start_node != end_node:
            print("ERROR")
            return
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        self.path = path[::-1]
        print(f"chemin : {self.path}")

            
            




if __name__ == "__main__":
    try:
        test = BFS()
        test.parse_file(sys.argv[len(sys.argv) - 1])
        test.get_path()
    except Exception as e:
        print(e)
